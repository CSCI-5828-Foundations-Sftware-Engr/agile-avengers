import React, { useState } from "react";
import Mandatory from "../../common/component/Mandatory";

const Signup = () => {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [errorMessage, setErrorMessage] = useState("");

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
    if (!validateEmail(username)) {
        setErrorMessage("Invalid email address");
        return;
    }
    if (password !== confirmPassword) {
        setErrorMessage("Passwords do not match");
        return;
      }
    
    
    fetch("/api/v1/auth/create", {
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
          return response.json();
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

  const validateEmail = (email) => {
    // basic email validation regex
    const regex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return regex.test(email);
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
                  <Mandatory>Email</Mandatory>
                </label>
                <input
                  type="email"
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
