import React, { useState, useRef, useEffect } from "react";
import "./Chat.css";
import { Button, IconButton } from "@mui/material";
import SendIcon from "@mui/icons-material/Send";

const App = () => {
  const localVideoRef = useRef(null);
  const remoteVideoRef = useRef(null);
  const signalingServer = useRef(null);
  const peerConnection = useRef(null);
  const ringAudioRef = useRef(null);
  const historyRef = useRef(null);
  const callTypeRef = useRef("video");

  const [senderId, setSenderId] = useState("");
  const [receiverId, setReceiverId] = useState("");
  const [callStatus, setCallStatus] = useState("idle");
  const [messages, setMessages] = useState([]);
  const [receivedMessages, setReceivedMessages] = useState([]);
  const [message, setMessage] = useState("");
  const [loading, setLoading] = useState(false);
  const [msg, setmsg] = useState([]);
  const [screenSharing, setScreenSharing] = useState(false);
  const screenStreamRef = useRef(null);

  const currentDate = new Date();
  const options = { hour: "2-digit", minute: "2-digit" };
  const timeString = currentDate.toLocaleTimeString(undefined, options);
  const [isScreenSharing, setIsScreenSharing] = useState(false);
  const screenTrackRef = useRef(null);

  const iceServers = [
    { urls: "stun:stun.relay.metered.ca:80" },
    {
      urls: "turn:global.relay.metered.ca:80",
      username: "b7ccc598c5ad0d92a7dbc2c2",
      credential: "ujv2zwyoJ0QyKATN",
    },
    {
      urls: "turn:global.relay.metered.ca:80?transport=tcp",
      username: "b7ccc598c5ad0d92a7dbc2c2",
      credential: "ujv2zwyoJ0QyKATN",
    },
    {
      urls: "turn:global.relay.metered.ca:443",
      username: "b7ccc598c5ad0d92a7dbc2c2",
      credential: "ujv2zwyoJ0QyKATN",
    },
    {
      urls: "turns:global.relay.metered.ca:443?transport=tcp",
      username: "b7ccc598c5ad0d92a7dbc2c2",
      credential: "ujv2zwyoJ0QyKATN",
    },
  ];

  const handleChange = (event) => {
    setSenderId(event.target.value);
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    setLoading(true);
    try {
      const response = await fetch(
        `http://localhost:8000/messaging/conversation_users_history/${senderId}/`
      );
      if (!response.ok) {
        throw new Error("Network response was not ok");
      }
      const data = await response.json();
      setmsg(data);
    } catch (error) {
      console.error("Error fetching conversation:", error);
    }
    setLoading(false);
  };

  useEffect(() => {
    if (senderId && receiverId) {
      getHistory();
      connectToSocket(senderId, receiverId);
    }

    // Cleanup on receiverId change
    return () => {
      setMessages([]);
      setReceivedMessages([]);
    };
  }, [senderId, receiverId]);

  const scrollToBottom = () => {
    if (historyRef.current) {
      setTimeout(() => {
        historyRef.current.scrollTop = historyRef.current.scrollHeight;
      }, 0);
    }
  };

const handleMessageSend = () => {
  if (
    signalingServer.current &&
    signalingServer.current.readyState === WebSocket.OPEN &&
    message.trim() !== ""
  ) {
    const messageData = {
      type: "chat_message",
      message,
      timestamp: new Date().toLocaleString(),
    };
    signalingServer.current.send(JSON.stringify(messageData));

    // Add the sent message to the local state
    setMessages((prevMessages) => [
      ...prevMessages,
      {
        content: message,
        timestamp: messageData.timestamp,
        sender: parseInt(senderId),
      },
    ]);

    setMessage("");
  }
};

const toggleScreenShare = async () => {
  if (!isScreenSharing) {
    try {
      const screenStream = await navigator.mediaDevices.getDisplayMedia({
        video: true,
      });
      const screenTrack = screenStream.getTracks()[0];
      screenTrackRef.current = screenTrack;

      const sender = peerConnection.current
        .getSenders()
        .find((s) => s.track.kind === "video");
      sender.replaceTrack(screenTrack);

      screenTrack.onended = () => {
        stopScreenShare();
      };

      setIsScreenSharing(true);
    } catch (error) {
      console.error("Error sharing screen:", error);
    }
  } else {
    stopScreenShare();
  }
};

const stopScreenShare = () => {
  if (screenTrackRef.current) {
    screenTrackRef.current.stop();
    const localStream = localVideoRef.current.srcObject;
    const localVideoTrack = localStream
      .getTracks()
      .find((track) => track.kind === "video");

    const sender = peerConnection.current
      .getSenders()
      .find((s) => s.track.kind === "video");
    sender.replaceTrack(localVideoTrack);

    screenTrackRef.current = null;
    setIsScreenSharing(false);
  }
};

const getHistory = async () => {
  try {
    const response = await fetch(
      `http://localhost:8000/messaging/api/chat/${receiverId}/${senderId}/history/`
    );
    if (!response.ok) throw new Error("Failed to fetch history");
    const result = await response.json();
    setMessages(result);
    scrollToBottom();
  } catch (error) {
    console.error("Error fetching history:", error.message);
  }
};

const connectToSocket = (senderId, receiverId) => {
  const signalingServerUrl = `ws://localhost:8000/ws/chat/${senderId}/${receiverId}/`;
  signalingServer.current = new WebSocket(signalingServerUrl);

  signalingServer.current.onmessage = async (message) => {
    const data = JSON.parse(message.data);
    console.log("Message from server:", data);

    if (data.type === "offer") {
      if (peerConnection.current.signalingState !== "stable") {
        console.error(
          "PeerConnection is not in a stable state:",
          peerConnection.current.signalingState
        );
        return;
      }
      callTypeRef.current = data.callType;
      await peerConnection.current.setRemoteDescription(
        new RTCSessionDescription(data.offer)
      );
      console.log("test");
      setCallStatus("ringing");
      ringAudioRef.current.play();
    } else if (data.type === "answer") {
      if (peerConnection.current.signalingState !== "have-local-offer") {
        console.error(
          "PeerConnection is not in a state to accept an answer:",
          peerConnection.current.signalingState
        );
        return;
      }
      await peerConnection.current.setRemoteDescription(
        new RTCSessionDescription(data.answer)
      );
      console.log("test2", data);

      setCallStatus("active");
    } else if (data.type === "ice_candidate") {
      try {
        await peerConnection.current.addIceCandidate(
          new RTCIceCandidate(data.candidate)
        );
      } catch (error) {
        console.error("Failed to add ICE candidate:", error);
      }
    } else if (data.type === "call_ended") {
      endCall();
    } else if (data.type === "chat_message") {
      setReceivedMessages((prev) => [...prev, data]);
    }
  };

  signalingServer.current.onopen = () => {
    console.log("Signaling server connected");
  };

  peerConnection.current = new RTCPeerConnection({ iceServers });

  peerConnection.current.onicecandidate = (event) => {
    if (event.candidate) {
      signalingServer.current.send(
        JSON.stringify({
          type: "ice_candidate",
          candidate: event.candidate,
          sender_id: senderId,
        })
      );
    }
  };

  peerConnection.current.ontrack = (event) => {
    remoteVideoRef.current.srcObject = event.streams[0];
  };
};

const startLocalStream = async () => {
  if (!peerConnection.current) {
    peerConnection.current = new RTCPeerConnection({ iceServers });
  }

  if (!signalingServer.current) {
    signalingServer.current = new WebSocket(
      `ws://localhost:8000/ws/chat/${senderId}/${receiverId}/`
    );
  }

  const localStream = await navigator.mediaDevices.getUserMedia({
    video: true,
    audio: true,
  });
  localVideoRef.current.srcObject = localStream;
  localStream
    .getTracks()
    .forEach((track) => peerConnection.current.addTrack(track, localStream));

  const offer = await peerConnection.current.createOffer();
  await peerConnection.current.setLocalDescription(offer);
  signalingServer.current.send(
    JSON.stringify({
      type: "offer",
      offer: offer,
      sender_id: senderId,
      receiver_id: receiverId,
      callType: "video",
    })
  );
  setCallStatus("active");
};

const startLocalAudioStream = async () => {
  if (!peerConnection.current) {
    peerConnection.current = new RTCPeerConnection({ iceServers });
  }

  if (!signalingServer.current) {
    signalingServer.current = new WebSocket(
      `ws://localhost:8000/ws/chat/${senderId}/${receiverId}/`
    );
  }

  const localStream = await navigator.mediaDevices.getUserMedia({
    audio: true,
  });
  localVideoRef.current.srcObject = localStream;
  localStream
    .getTracks()
    .forEach((track) => peerConnection.current.addTrack(track, localStream));

  const offer = await peerConnection.current.createOffer();
  await peerConnection.current.setLocalDescription(offer);
  signalingServer.current.send(
    JSON.stringify({
      type: "offer",
      offer: offer,
      sender_id: senderId,
      callType: "audio",
    })
  );
  setCallStatus("active");
};

const stopScreenSharing = () => {
  screenStreamRef.current.getTracks().forEach((track) => track.stop());
  screenStreamRef.current = null;
  setScreenSharing(false);
};

const acceptCall = async () => {
  ringAudioRef.current.pause();
  ringAudioRef.current.currentTime = 0;

  const localStream = await navigator.mediaDevices.getUserMedia({
    video: callTypeRef.current === "video",
    audio: true,
  });
  localVideoRef.current.srcObject = localStream;
  localStream
    .getTracks()
    .forEach((track) => peerConnection.current.addTrack(track, localStream));

  const answer = await peerConnection.current.createAnswer();
  await peerConnection.current.setLocalDescription(answer);
  signalingServer.current.send(
    JSON.stringify({ type: "answer", answer: answer, sender_id: senderId })
  );
  setCallStatus("active");
};

const endCall = () => {
  if (localVideoRef.current.srcObject) {
    localVideoRef.current.srcObject
      .getTracks()
      .forEach((track) => track.stop());
    localVideoRef.current.srcObject = null;
  }

  if (peerConnection.current) {
    peerConnection.current.close();
    peerConnection.current = null;
  }

  if (signalingServer.current) {
    signalingServer.current.send(
      JSON.stringify({ type: "call_ended", sender_id: senderId })
    );
    signalingServer.current.close();
    signalingServer.current = null;
  }

  if (ringAudioRef.current) {
    ringAudioRef.current.pause();
    ringAudioRef.current.currentTime = 0;
  }

  if (screenSharing) {
    stopScreenSharing();
  }

  connectToSocket(senderId, receiverId);
  setCallStatus("idle");
};

console.log("receivedMessages:", receivedMessages);
console.log("senderId:", senderId);

const filteredMessages = receivedMessages.filter((msg) => {
  console.log("Checking message:", msg);

  return msg.receiver_id === senderId;
});

console.log("filteredMessages:", filteredMessages);
return (
  <div className={`App ${callStatus === "active" ? "call-active" : ""}`}>
    <div className="videocalldisplay">
      <div className="localvideo">
        <video ref={localVideoRef} autoPlay muted className="video"></video>
      </div>
      <div className="remotvideo">
        <video ref={remoteVideoRef} autoPlay className="video"></video>
      </div>
    </div>
    {callStatus !== "active" && (
      <div className="conversation-container">
        <form onSubmit={handleSubmit}>
          <label htmlFor="sender-id">Enter sender ID:</label>
          <input
            id="sender-id"
            type="text"
            value={senderId}
            onChange={handleChange}
          />
          <button className="fetch-conversation-button" type="submit">
            Fetch Conversation
          </button>
        </form>
        {loading && <p>Loading...</p>}
        <ul className="message-list">
          {msg.map((message, index) => (
            <li
              key={index}
              className={
                message.sender === senderId
                  ? "received-message"
                  : "sent-message"
              }
            >
              <button
                className="conversation-button"
                onClick={() => setReceiverId(message.id)}
              >
                {message.username}
              </button>
            </li>
          ))}
        </ul>
      </div>
    )}

    <div className="chat-history" ref={historyRef}>
      <div className="video-call-container">
        {(callStatus === "idle" || callStatus === "ended") && (
          <>
            <img
              style={{ width: "30px", height: "30px" }}
              onClick={() => {
                callTypeRef.current = "video";
                startLocalStream();
              }}
              src={process.env.PUBLIC_URL + "video-camera.png"}
              alt="Video Call"
            />
            <img
              style={{ width: "30px", height: "30px" }}
              onClick={() => {
                callTypeRef.current = "audio";
                startLocalAudioStream();
              }}
              src={process.env.PUBLIC_URL + "phone-call.png"}
              alt="Voice Call"
            />
          </>
        )}
        {callStatus === "ringing" && (
          <>
            <button onClick={acceptCall}>Accept Call</button>
            <button className="end-call" onClick={endCall}>
              End Call
            </button>
          </>
        )}
        {callStatus === "active" && (
          <div className="call-controls">
            <button className="end-call" onClick={endCall}>
              End Call
            </button>
            {callTypeRef.current === "video" ? (
              <button className="screen-share" onClick={toggleScreenShare}>
                {isScreenSharing ? (
                  <img
                    style={{ width: "30px", height: "30px" }}
                    src={process.env.PUBLIC_URL + "screen-share.png"}
                  />
                ) : (
                  <img
                    style={{ width: "30px", height: "30px" }}
                    src={process.env.PUBLIC_URL + "stop-screen-share.png"}
                  />
                )}
              </button>
            ) : (
              ""
            )}
          </div>
        )}

        <audio
          ref={ringAudioRef}
          src={process.env.PUBLIC_URL + "messenger_video_call.mp3"}
          loop
        ></audio>
      </div>

      <ul className="message-list">
        {messages.map((msg, index) => (
          <li
            key={index}
            className={`message-item ${
              msg.sender === parseInt(senderId) ? "receiver" : "sender"
            }`}
          >
            <div className="message-content">
              <div className="message-text">{msg.content}</div>

              <div className="message-timestamp">
                {new Date(msg.timestamp).toLocaleTimeString([], {
                  hour: "2-digit",
                  minute: "2-digit",
                  hour12: true,
                })}
              </div>
            </div>
          </li>
        ))}
        {receivedMessages
          .filter(
            (msg) => msg.receiver_id == senderId && msg.sender_id == receiverId
          )
          .map((msg, index) => (
            <li
              key={index}
              className={`message-item new-message ${
                msg.sender_id === senderId ? "receiver" : "sender"
              }`}
            >
              <div className="message-content">
                <div className="message-text">{msg.message}</div>
                <div className="message-timestamp">{timeString}</div>
              </div>
            </li>
          ))}
      </ul>
      <div className="input-container">
        <input
          type="text"
          value={message}
          onChange={(e) => setMessage(e.target.value)}
          placeholder="Type your message..."
        />
        <IconButton
          className="btn-primary"
          variant="contained"
          color="primary"
          onClick={handleMessageSend}
          sx={{ width: "10%", color: "#000" }}
        >
          <SendIcon fontSize="large" />
        </IconButton>
      </div>
    </div>
  </div>
);
};

export default App;
