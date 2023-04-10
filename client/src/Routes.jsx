import React from "react";
import { Route, Switch } from "react-router-dom";
import propTypes from "prop-types";
import Home from "./component/Home/Home";
import New from "./component/Payment/New";
import Login from "./component/Login/Login";
import Signup from "./component/Signup/Signup";

const Routes = () => (
  <Switch>
    <Route exact path="/" component={Home} />
    <Route exact path="/payment" component={New} />
    <Route exact path="/login" component={Login} />
    <Route exact path="/signup" component={Signup} />

  </Switch>
);

Routes.propTypes = {
  permissions: propTypes.shape({}).isRequired
};

export default Routes;
