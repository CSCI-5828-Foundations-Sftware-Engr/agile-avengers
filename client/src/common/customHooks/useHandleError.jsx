import React, { useContext } from "react";
import NotFoundContext from "../contexts/notFoundContext";
import { showToast } from "../component/ToastContainer";
import { PlainToastMessage } from "../component/ToastMessage";
import { errorHandling } from "../errorHandling";

const useErrorHandling = error => {
  const { setNotFound } = useContext(NotFoundContext);
  let errorHandled = false;
  if (error) {
    if (error && error.response) {
      if (error.response.status === 404) {
        setNotFound({ notFound: true, type: 404 });
        errorHandled = true;
      }
      if (error.response.status === 401) {
        setNotFound({ notFound: true, type: 401 });
        errorHandled = true;
      }
    }
    if (!errorHandled) {
      showToast({
        type: "error",
        message: <PlainToastMessage message={errorHandling(error)} />
      });
    }
  }
  return null;
};
export default useErrorHandling;
