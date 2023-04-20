import React, { useContext } from "react";
import NavigationItem from "../common/component/NavigationItem";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faUser, faSignOutAlt } from "@fortawesome/free-solid-svg-icons"; // 1. Import the faSignOutAlt icon
import { faFontAwesome } from "@fortawesome/free-brands-svg-icons";
import { AuthContext } from "./Context/Authcontext";

import Routes from "../Routes";

const Container = () => {
  const { isLoggedIn, setIsLoggedIn } = useContext(AuthContext);

  // 2. Add a handleLogout function to handle the logout logic
  const handleLogout = () => {
    setIsLoggedIn(false);
    localStorage.removeItem("access_token");
    window.location.href = "/login";
  };

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
          
          {isLoggedIn ? (
            <>
              <NavigationItem link="/payment">
                Send or Request Payment
              </NavigationItem>
              <NavigationItem link="/add_payment_method">
                Add Payment Methods
              </NavigationItem>
              <NavigationItem link="/transaction">
                Transactions
              </NavigationItem>
              {/* 4. Conditionally render the logout link on the right */}
              <a onClick={handleLogout} className="ml-auto">
                <FontAwesomeIcon icon={faSignOutAlt} /> Logout
              </a>
            </>
          ) : (
            <>
              <NavigationItem link="/login">Login</NavigationItem>
              <NavigationItem link="/signup">Sign Up</NavigationItem>
            </>
          )}
        </ul>
      </div>
      <div className="body-content">
        <Routes />
      </div>
      <footer>
        <div className="footer">
          <span>
            <a className="link-white" href="mailto:agileavengers@gmail.com">
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
