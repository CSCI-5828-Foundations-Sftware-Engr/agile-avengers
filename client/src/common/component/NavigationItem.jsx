import React from "react";
import PropTypes from "prop-types";
import { NavLink } from "react-router-dom";

const NavigationItem = ({ exact, link, className, children }) => (
  <li className={className}>
    <NavLink exact={exact} to={link}>
      {children}
    </NavLink>
  </li>
);

NavigationItem.defaultProps = {
  exact: false,
  className: "",
  children: null
};

NavigationItem.propTypes = {
  exact: PropTypes.bool,
  link: PropTypes.string.isRequired,
  className: PropTypes.string,
  children: PropTypes.node
};

export default NavigationItem;
