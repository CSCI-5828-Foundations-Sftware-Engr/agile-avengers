import React from "react";
import PropTypes from "prop-types";
import { CircleLoading } from "react-loadingg";

const LoaderComponent = ({ loader }) => {
  return (
    <div
      className="loader-container"
      style={{
        display: loader ? "block" : "none"
      }}
    >
      <CircleLoading
        color="#5976b2 !important"
        style={{
          margin: "10px auto",
          position: "relative"
        }}
      />
    </div>
  );
};

LoaderComponent.propTypes = {
  loader: PropTypes.bool.isRequired
};

export default LoaderComponent;
