import React from "react";
import PropTypes from "prop-types";
import { LoopCircleLoading } from "react-loadingg";

const Spinner = ({ loadingSpinner }) => {
  return (
    <div
      className="loaderWrapper"
      style={{
        display: loadingSpinner ? "block" : "none"
      }}
    >
      <div className="loader">
        <LoopCircleLoading color="#365084" size="large" />
      </div>
    </div>
  );
};

Spinner.propTypes = {
  loadingSpinner: PropTypes.string.isRequired
};

export default Spinner;
