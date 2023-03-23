import React from "react";
import PropTypes from "prop-types";

import { Button } from "react-bootstrap";
import { confirmAlert } from "react-confirm-alert"; // Import
import "react-confirm-alert/src/react-confirm-alert.css"; // Import css

export const showConfirmationAndDelete = options => {
  confirmAlert({
    customUI: ({ onClose }) => (
      <Confirmation
        data={options.data}
        msg={options.message}
        onClose={onClose}
        onYesAction={options.onYesAction}
      />
    )
  });
};

export const Confirmation = ({ msg, onYesAction, onClose, data }) => {
  return (
    <div className="confirmBox">
      <h4>Confirm!</h4>
      {msg}
      <br />
      <br />
      <div>
        <Button
          onClick={() => {
            onYesAction(data);
            onClose();
          }}
        >
          <div>Yes</div>
        </Button>
        <Button variant="light" onClick={onClose}>
          <div>No</div>
        </Button>
      </div>
    </div>
  );
};

Confirmation.propTypes = {
  msg: PropTypes.string.isRequired,
  onYesAction: PropTypes.func.isRequired,
  onClose: PropTypes.func.isRequired,
  data: PropTypes.shape({}).isRequired
};

export default Confirmation;
