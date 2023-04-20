import { faLess } from "@fortawesome/free-brands-svg-icons";
import React, { useContext, useState, useEffect } from "react";
import Mandatory from "../../common/component/Mandatory";
import { AuthContext } from "../Context/Authcontext";
import { useHistory } from "react-router-dom";
import Cookies from 'universal-cookie';
import { BACKEND_API_URL } from "../../constants/backend";


const Login = (props) => {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [errorMessage, setErrorMessage] = useState("");
  const {isLoggedIn, setIsLoggedIn} = useContext(AuthContext);
  const queryParams = new URLSearchParams(props.location.search);
  const success = queryParams.get('success');


  const handleUsernameChange = (event) => {
    setUsername(event.target.value);
  };

  const handlePasswordChange = (event) => {
    setPassword(event.target.value);
  };

  const history = useHistory();

  const handleSubmit = (event) => {
    event.preventDefault();
<<<<<<< Updated upstream
    fetch(`${BACKEND_API_URL}/auth/login`, {
    // fetch("http://127.0.0.1:5000/api/v1/auth/login", {
=======
    fetch("http://127.0.0.1/api/v1/auth/login", {
>>>>>>> Stashed changes
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
        // const cookies = new Cookies();
        // cookies.set('access_token', data.token.access_token, { path: '/' });
        // cookies.set('refresh_token', data.token.refresh_token, { path: '/' });
        localStorage.setItem('access_token', data.token.access_token);
        localStorage.setItem('refresh_token', data.token.refresh_token);
        localStorage.setItem('user_id', data.user_id);
        history.push("/payment");
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
        {success && (
                <div className="alert alert-success">{"Account created successfully"}</div>
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
