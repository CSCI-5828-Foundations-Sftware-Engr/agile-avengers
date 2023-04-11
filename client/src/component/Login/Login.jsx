import { faLess } from "@fortawesome/free-brands-svg-icons";
import React, { useContext, useState } from "react";
import Mandatory from "../../common/component/Mandatory";
import { AuthContext } from "../Context/Authcontext";

const Login = () => {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [errorMessage, setErrorMessage] = useState("");
  const {isLoggedIn, setIsLoggedIn} = useContext(AuthContext);


  const handleUsernameChange = (event) => {
    setUsername(event.target.value);
  };

  const handlePasswordChange = (event) => {
    setPassword(event.target.value);
  };

  const handleSubmit = (event) => {
    event.preventDefault();
    fetch("/api/v1/auth/login", {
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
          setIsLoggedIn(true);
          return response.json();
        } else {
          throw new Error("Wrong credentials");
        }
      })
      .then((data) => {
        // handle successful login
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
        {errorMessage && (
                <div className="alert alert-danger">{errorMessage}</div>
              )}
        <br />
        <br />
        <div className="card">
          <div className="card-header back-light-primary text-white">
            Login
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
                <button
                  type="submit"
                  className="btn btn-primary float-right"
                >
                  Login
                </button>
                New User? <a href="/signup"> Signup here </a>
              </div>
              
            </form>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Login;
