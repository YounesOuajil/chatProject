// VideoCallModal.js
import React from "react";
import Modal from "react-modal";

Modal.setAppElement("#root"); // Set the root element for accessibility

const VideoCallModal = ({
  isOpen,
  onRequestClose,
  localVideoRef,
  remoteVideoRef,
  callStatus,
  startLocalStream,
  acceptCall,
  endCall,
}) => (
  <Modal
    isOpen={isOpen}
    onRequestClose={onRequestClose}
    contentLabel="Video Call"
    className="video-call-modal"
    overlayClassName="video-call-overlay"
  >
    <div className="video-call-container">
      {callStatus === "idle" || callStatus === "ended" ? (
        <button onClick={startLocalStream}>Start Call</button>
      ) : callStatus === "ringing" ? (
        <>
          <button onClick={acceptCall}>Accept Call</button>
          <button onClick={endCall}>End Call</button>
        </>
      ) : (
        <button onClick={endCall}>End Call</button>
      )}
      <video ref={localVideoRef} autoPlay muted className="video"></video>
      <video ref={remoteVideoRef} autoPlay className="video"></video>
    </div>
  </Modal>
);

export default VideoCallModal;
