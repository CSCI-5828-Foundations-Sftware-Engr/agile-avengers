import React, { useState, useEffect } from "react";
import PropTypes from "prop-types";
import Mandatory from "../../common/component/Mandatory";

const UserInfo = ({ username }) => {
  const [userData, setUserData] = useState(null);
  const [errorMessage, setErrorMessage] = useState("");

  useEffect(() => {
    fetch(`/api/v1/users/get?username=${username}`)
      .then((response) => {
        if (response.ok) {
          return response.json();
        } else {
          throw new Error("Unable to fetch user info");
        }
      })
      .then((data) => {
        setUserData(data);
      })
      .catch((error) => {
        setErrorMessage(error.message);
      });
  }, [username]);

  return (
    <div className="container-flex">
      <div className="container">
        <br />
        <br />
        <div className="card">
          <div className="card-header back-light-primary text-white">
            User Info
          </div>
          <div className="card-body">
            {userData ? (
              <div>
                <p>
                  <strong>First Name:</strong> {userData.first_name}
                </p>
                <p>
                  <strong>Last Name:</strong> {userData.last_name}
                </p>
                <p>
                  <strong>Mobile Number:</strong> {userData.mobile_number}
                </p>
                <p>
                  <strong>Is Merchant:</strong> {userData.is_merchant ? "Yes" : "No"}
                </p>
              </div>
            ) : (
              <p>Loading user info...</p>
            )}
            {errorMessage && (
              <div className="alert alert-danger">{errorMessage}</div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

UserInfo.propTypes = {
  username: PropTypes.string.isRequired,
};

export default UserInfo;
