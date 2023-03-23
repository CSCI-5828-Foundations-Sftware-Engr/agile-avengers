import React, { useContext } from "react";

import SpinnerContext from "../contexts/spinnerContext";
import NotFoundContext from "../contexts/notFoundContext";

const NotFound = () => {
  const spinner = useContext(SpinnerContext);
  const { setNotFound } = useContext(NotFoundContext);
  spinner.setShowLoader(false);
  setNotFound(true);

  return (
    <div className="float-center">
      <h1 className="not-found">404 Not Found</h1>
      <p>The page which you are looking for does not exist</p>
    </div>
  );
};

export default NotFound;
