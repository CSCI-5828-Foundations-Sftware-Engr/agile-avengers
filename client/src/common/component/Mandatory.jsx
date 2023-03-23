import React from "react";
import PropTypes from "prop-types";

const Mandatory = ({ children }) => (
  <>
    <div className="mandatory" /> {children}
  </>
);

Mandatory.defaultProps = {
  children: ""
};

Mandatory.propTypes = {
  children: PropTypes.node
};

export default Mandatory;
