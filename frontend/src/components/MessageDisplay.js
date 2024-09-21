import React from 'react';
const MessageDisplay = React.memo(({ statusMessage }) => {
    return (
      <div>
        {statusMessage && <p style={{ color: 'green' }}>{statusMessage}</p>}
      </div>
    );
  });

  export default MessageDisplay;