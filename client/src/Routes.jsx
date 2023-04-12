import React from "react";
import { Route, Switch } from "react-router-dom";
import propTypes from "prop-types";
import Home from "./component/Home/Home";
import NewPayment from "./component/Payment/NewPayment";
import AddPaymentMethod from "./component/PaymentMethod/AddPaymentMethod";
import Login from "./component/Login/Login";
import Signup from "./component/Signup/Signup";
import CreateUser from "./component/UserInfo/CreateUser";

const Routes = () => (
  <Switch>
    <Route exact path="/" component={Home} />
    <Route exact path="/payment" component={NewPayment} />
    <Route exact path="/add_payment_method" component={AddPaymentMethod} />
    <Route exact path="/login" component={Login} />
    <Route exact path="/signup" component={Signup} />
    <Route exact path="/createuser" component={CreateUser} />
  </Switch>
);

Routes.propTypes = {
  permissions: propTypes.shape({}).isRequired
};

export default Routes;
