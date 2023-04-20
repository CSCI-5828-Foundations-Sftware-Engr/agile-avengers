import React, { useState } from "react";
import { useHistory } from "react-router-dom";
import Mandatory from "../../common/component/Mandatory";
import { BACKEND_API_URL } from "../../constants/backend";

const Signup = () => {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [errorMessage, setErrorMessage] = useState("");
  const history = useHistory();


  const handleUsernameChange = (event) => {
    setUsername(event.target.value);
  };

  const handlePasswordChange = (event) => {
    setPassword(event.target.value);
  };

  const handleConfirmPasswordChange = (event) => {
    setConfirmPassword(event.target.value);
  };

  const handleSubmit = (event) => {
    event.preventDefault();
   
    if (password !== confirmPassword) {
        setErrorMessage("Passwords do not match");
        return;
      }
    
    // fetch("http://127.0.0.1:5000/api/v1/auth/create", {
    fetch(`${BACKEND_API_URL}/auth/create`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        username,
        password
      })
    })
      .then((response) => {
        if (response.ok) {
            history.push(`/createuser?username=${username}`);
        } else if (response.status === 409) {
          throw new Error("User already exists");
        } else {
          throw new Error("Unable to create user");
        }
      })
      .then((data) => {
        // handle successful user creation
        console.log(data.message);
      })
      .catch((error) => {
        setErrorMessage(error.message);
      });
  };



  return (
    <div className="container-flex">
      <div className="container">
      <br />
      <div>
        {errorMessage && (
          <div className="alert alert-danger">{errorMessage}</div>
        )}
        </div>
        <br />
        <br />
        <div className="card">
          <div className="card-header back-light-primary text-white">
            Create Account
          </div>
          <div className="card-body">
            <form onSubmit={handleSubmit}>
              <div className="form-group">
                <label htmlFor="username">
                  <Mandatory>Username</Mandatory>
                </label>
                <input
                  type="text"
                  className="form-control"
                  id="username"
                  value={username}
                  onChange={handleUsernameChange}
                />
              </div>
              <div className="form-group">
                <label htmlFor="password">
                  <Mandatory>Password</Mandatory>
                </label>
                <input
                  type="password"
                  className="form-control"
                  id="password"
                  value={password}
                  onChange={handlePasswordChange}
                />
              </div>
              <div className="form-group">
                <label htmlFor="confirmPassword">
                  <Mandatory>Confirm Password</Mandatory>
                </label>
                <input
                  type="password"
                  className="form-control"
                  id="confirmPassword"
                  value={confirmPassword}
                  onChange={handleConfirmPasswordChange}
                />
                </div>
              <div className="form-group">
                <button
                  type="submit"
                  className="btn btn-primary float-right"
                >
                  Sign Up
                </button>
              </div>

            </form>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Signup;