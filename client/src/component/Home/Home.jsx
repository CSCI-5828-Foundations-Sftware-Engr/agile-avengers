import React from "react";
import { Redirect } from "react-router-dom";

const Home = () => {
  return (
    <div>
      <Redirect to="/login/"/>
      {/* <Redirect to="/payment/" /> */}
    </div>
  );
};
export default Home;
