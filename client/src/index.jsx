import React from "react";
import ReactDOM from "react-dom";
import { BrowserRouter } from "react-router-dom";
import App from "./component/App";
import AuthProvider from "./component/Context/Authcontext"

ReactDOM.render(
  <div>
    <BrowserRouter>
        <App />
      
    </BrowserRouter>
  </div>,
  document.getElementById("root")
);
