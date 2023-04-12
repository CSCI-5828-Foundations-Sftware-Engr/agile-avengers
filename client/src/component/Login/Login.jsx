import { faLess } from "@fortawesome/free-brands-svg-icons";
import React, { useContext, useState } from "react";
import Mandatory from "../../common/component/Mandatory";
import { AuthContext } from "../Context/Authcontext";
import Cookies from 'universal-cookie';


const Login = () => {
    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");
    const [errorMessage, setErrorMessage] = useState("");
    const { isLoggedIn, setIsLoggedIn } = useContext(AuthContext);
    const [authToken, setAuthToken] = useState(null);


    const handleUsernameChange = (event) => {
        setUsername(event.target.value);
    };

    const handlePasswordChange = (event) => {
        setPassword(event.target.value);
    };

    const handleSubmit = (event) => {
        event.preventDefault();
        fetch("http://127.0.0.1:5000/api/v1/auth/login", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*",
                "Accept":  "*/*"
            },
            body: JSON.stringify({
                username,
                password
            })
        }).then(response => response.json())
        .then(data => {

            console.log(data);
            const cookies = new Cookies();
            cookies.set('access_token', data.token.access_token, { path: '/' });
            cookies.set('refresh_token', data.tokenrefresh_token, { path: '/' });

            // console.log(document.cookie);
            // cookies.get('myCat');
            // console.log(cookies.get('auth_token'))
                // handle successful login
                    // retrieve the auth_token cookie
    //             const cookies = document.cookie.split(";").reduce((prev, current) => {
    //     const [name, value] = current.trim().split("=");
    //     return { ...prev, [name]: value };
    //   }, {});
  
      // use the token to make authenticated requests
    //   console.log(cookies.auth_token);
                // console.log(data.message);
                // const cookieString = document.cookie;
                // console.log(cookieString);
                // const cookies = cookieString.split(';');
                // for (let i = 0; i < cookies.length; i++) {
                //   const cookie = cookies[i].trim();
                //   if (cookie.startsWith('auth_token=')) {
                //     const authTokenValue = cookie.substring('auth_token='.length);
                //     setAuthToken(JSON.parse(authTokenValue));
                //     break;
                //   }
                // }
                setIsLoggedIn(true);
            })
            .catch((error) => {
                setErrorMessage(error.message);
            });
    };

    const handleTest = (event) => {
        event.preventDefault();
        fetch("http://127.0.0.1:5000/api/v1/auth/userinfo", {
            method: "GET",
            headers: {
                "Content-Type": "application/json"
            },
            credentials: 'include',
            mode: 'cors'
        }).then((data) => {
            console.log("userinfo sucess!!!!!!!")
            console.log(data);
                // handle successful login
                console.log(data);
                setIsLoggedIn(true);
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
                        <button className="btn btn-primary" onClick={handleTest}>Userinfo</button>
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
                                <button type="submit" className="btn btn-primary float-right">
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