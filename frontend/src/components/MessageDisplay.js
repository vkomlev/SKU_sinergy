const MessageDisplay = ({ statusMessage }) => {
    return (
      <div>
        {statusMessage && <p style={{ color: 'green' }}>{statusMessage}</p>}
      </div>
    );
  };

  export default MessageDisplay;