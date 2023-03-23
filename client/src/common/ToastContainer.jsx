import React from "react";
import PropTypes from "prop-types";
import toaster from "toasted-notes";
import { FaRegCheckCircle, FaRegTimesCircle } from "react-icons/fa";
import { IoMdInformationCircleOutline } from "react-icons/io";
import { utils } from "./utils";
import { TOAST } from "./constants";

export const showToast = (options) => {
  switch (options.type) {
    case "success": {
      toaster.notify(
        ({ onClose }) => (
          <SuccessToastContainer onClose={onClose} message={options.message} />
        ),
        {
          duration:
            options.duration !== null ? options.duration || TOAST.TIMER : null,
          position: options.position,
        }
      );
      break;
    }

    case "error": {
      toaster.notify(
        ({ onClose }) => (
          <ErrorToastContainer onClose={onClose} message={options.message} />
        ),
        {
          duration:
            options.duration !== null ? options.duration || TOAST.TIMER : null,
          position: options.position,
        }
      );
      break;
    }

    default: {
      toaster.notify(
        ({ onClose }) => (
          <InfoToastContainer onClose={onClose} message={options.message} />
        ),
        {
          duration:
            options.duration !== null ? options.duration || TOAST.TIMER : null,
          position: options.position,
        }
      );
      break;
    }
  }
};

const SuccessToastContainer = ({ onClose, message }) => {
  return (
    <div className="mains">
      <div className="toast_common">
        <div className="toast_col1">
          <FaRegCheckCircle size="1.8em" color="white" />
        </div>
        <div className="toast_col2">{message}</div>
        <div className="toast_col3" {...utils.buttonize(onClose)}>
          ✕
        </div>
      </div>
      <br />
    </div>
  );
};

const ErrorToastContainer = ({ onClose, message }) => {
  return (
    <div className="mains">
      <div className="toast_common">
        <div className="toast_col1" style={{ backgroundColor: "red" }}>
          <FaRegTimesCircle size="1.8em" color="white" />
        </div>
        <div className="toast_col2">{message}</div>
        <div className="toast_col3" {...utils.buttonize(onClose)}>
          ✕
        </div>
      </div>
      <br />
    </div>
  );
};

const InfoToastContainer = ({ onClose, message }) => {
  return (
    <div className="mains">
      <div className="toast_common">
        <div className="toast_col1" style={{ backgroundColor: "#249aca" }}>
          <IoMdInformationCircleOutline size="2em" color="white" />
        </div>
        <div className="toast_col2">{message}</div>
        <div className="toast_col3" {...utils.buttonize(onClose)}>
          ✕
        </div>
      </div>
      <br />
    </div>
  );
};

export default showToast;

SuccessToastContainer.propTypes = {
  onClose: PropTypes.func.isRequired,
  message: PropTypes.shape({}).isRequired,
};

ErrorToastContainer.propTypes = {
  onClose: PropTypes.func.isRequired,
  message: PropTypes.shape({}).isRequired,
};

InfoToastContainer.propTypes = {
  onClose: PropTypes.func.isRequired,
  message: PropTypes.shape({}).isRequired,
};
