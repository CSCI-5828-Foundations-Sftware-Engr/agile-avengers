import React from "react";
import { Route, Switch } from "react-router-dom";
import propTypes from "prop-types";
import Home from "./component/Home/Home";
import New from "./component/Payment/New";

const Routes = () => (
  <Switch>
    <Route exact path="/" component={Home} />
    <Route exact path="/payment" component={New} />
  </Switch>
);

Routes.propTypes = {
  permissions: propTypes.shape({}).isRequired
};

export default Routes;
