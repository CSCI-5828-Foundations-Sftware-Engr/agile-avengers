import React, { useContext } from "react";
import NavigationItem from "../common/component/NavigationItem";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faUser } from "@fortawesome/free-solid-svg-icons";
import { faFontAwesome } from "@fortawesome/free-brands-svg-icons";

import Routes from "../Routes";

const Container = () => {
  return (
    <div>
      <header>
        <div className="header">
          <div className="easy-pay-logo-container float-left">
            <img
              src={`${window.location.origin}/client/easy-pay-logo.png`}
              alt="Easy Pay Logo"
            />
          </div>
          <span className="center-text header-title header-heading">
            <FontAwesomeIcon icon={faFontAwesome} /> Easy Pay
          </span>
        </div>
      </header>
      <div className="position-relative">
        <ul className="nav nav-tabs">
          
          <NavigationItem link="/payment">Payment</NavigationItem>
          {/* <NavigationItem link="/logout">Log Out</NavigationItem> */}
        </ul>
      </div>
      <div className="body-content">
        <Routes />
      </div>
      <footer>
        <div className="footer">
          <span>
            <a className="link-white" href="mailto:hemanth@colorado.com?cc=rudh9897@colorado.edu,aija">
              Contact us
            </a>
          </span>
          <div className="floatright">
            <span>Copyright © Easy Pay, Inc. All rights reserved.</span>
          </div>
        </div>
      </footer>
      <div />
    </div>
  );
};
export default Container;
