import React, { useEffect, useReducer, useState, useContext } from "react";
import { Prompt } from "react-router-dom";
import PropTypes from "prop-types";
import { Button } from "react-bootstrap";
import { errorHandling } from "../../common/errorHandling";
import { utils } from "../../common/utils";
import CONSTANTS from "../../common/constants";
import PermissionContext from "../../common/contexts/permissionContext";
import SpinnerConext from "../../common/contexts/spinnerContext";
import NotFoundContext from "../../common/contexts/notFoundContext";
import { sendReducer, initialState } from "../../reducers/sendReducer";
import sendService from "../../services/payment/sendService";
import {
  UPDATE_SUCCESS,
  SHOW_ERROR
} from "../../common/actions/SendReturnerTypes";
import useErrorHandling from "../../common/customHooks/useHandleError";

import { showToast } from "../../common/component/ToastContainer";
import {
  UpdatedSuccessToastMessage,
  PlainToastMessage
} from "../../common/component/ToastMessage";

const RequestPayment = props => {
  // const permissions = useContext(PermissionContext);
  // const spinner = useContext(SpinnerConext);
  // const { setNotFound } = useContext(NotFoundContext);
  // const [error, setError] = useState();
  // useErrorHandling(error);

  // const [access, setAccess] = useState(false);
  // const [disableSave, setDisabledSave] = useState(true);
  // const [orgInfo, setOrgInfo] = useState([]);
  // const [state, dispatch] = useReducer(applicationReducer, initialState);
  // const actions = (type, payload) => dispatch({ type, payload });
  // const { match } = props;

  // const getAllTheOrg = () => {
  //   spinner.setShowLoader(true);
  //   return getOrgList()
  //     .then(response => {
  //       setOrgInfo(response.data);
  //       spinner.setShowLoader(false);
  //     })
  //     .catch(err => {
  //       spinner.setShowLoader(false);
  //       showToast({
  //         type: "error",
  //         message: <PlainToastMessage message={errorHandling(err)} />
  //       });
  //     });
  // };

  // useEffect(() => {
  //   spinner.setShowLoader(true);
  //   Promise.all([
  //     getAllTheOrg(),
  //     getApplicationById(match.params.applicationId)
  //       .then(response => response.data)
  //       .then(data => {
  //         if (!data) {
  //           setNotFound({ notFound: true, type: 404 });
  //           spinner.setShowLoader(false);
  //           return;
  //         }

  //         const appDetail = {
  //           name: data.name,
  //           owner: data.owner,
  //           type: data.type,
  //           org: data.org,
  //           createdBy: data.data,
  //           createdAt: data.createdAt,
  //           updatedAt: data.updatedAt,
  //           id: data.id,
  //           createdUser: data.createdUser.fullname
  //         };
  //         actions(DATA_FETCH, appDetail);
  //         const permission = auth.authorize(
  //           PERMISSIONS_CONSTANTS.RESOURCE.APPLICATIONS,
  //           PERMISSIONS_CONSTANTS.ACTION.EDIT,
  //           "",
  //           permissions,
  //           data.name
  //         );
  //         setAccess(!permission);
  //         spinner.setShowLoader(false);
  //       })
  //       .catch(err => {
  //         setError(err);
  //         spinner.setShowLoader(false);
  //       })
  //   ]);
  // }, [match.params.applicationId]);

  // const alertUser = e => {
  //   e.preventDefault();
  //   e.returnValue = "There are unsaved changes, do you want to discard them?";
  // };

  // useEffect(() => {
  //   if (disableSave) {
  //     return undefined;
  //   }
  //   window.addEventListener("beforeunload", alertUser);
  //   return () => {
  //     window.removeEventListener("beforeunload", alertUser);
  //   };
  // }, [disableSave]);

  // const handleTextChange = e => {
  //   setDisabledSave(false);
  //   actions(APP_DETAIL_UPDATE_FORM, {
  //     target: e.target.name,
  //     value: e.target.value
  //   });
  // };

  // const updateApp = () => {
  //   const payload = {
  //     name: state.data.name,
  //     owner: state.data.owner,
  //     type: state.data.type,
  //     org: state.data.org
  //   };
  //   applicationSchema
  //     .validate(payload, { abortEarly: false })
  //     .then(() => {
  //       spinner.setShowLoader(true);
  //       updateApplication(match.params.applicationId, payload)
  //         .then(response => {
  //           setDisabledSave(true);
  //           spinner.setShowLoader(false);
  //           showToast({
  //             type: "success",
  //             message: (
  //               <UpdatedSuccessToastMessage
  //                 object="application"
  //                 recordName={state.data.name}
  //               />
  //             )
  //           });
  //           props.actions(RERENDER);
  //           actions(UPDATE_SUCCESS, response.data);
  //         })
  //         .catch(err => {
  //           spinner.setShowLoader(false);
  //           showToast({
  //             type: "error",
  //             message: <PlainToastMessage message={errorHandling(err)} />
  //           });
  //         });
  //     })
  //     .catch(errors => {
  //       actions(APPLICATION_SHOW_ERROR, utils.processValidationError(errors));
  //     });
  // };

  return (
    <div>
      <h1>Request Payment</h1>
    </div>
    //   <div>
    //     <Prompt
    //       when={!disableSave}
    //       message="There are unsaved changes, do you want to discard them?"
    //     />
    //     <div id="detailstab" className="formpanel">
    //       <div className="form-group">
    //         <label id="label-name" htmlFor="name">
    //           Name <span style={{ color: "red" }}>*</span>:
    //         </label>
    //         <input
    //           type="text"
    //           className="form-control"
    //           name="name"
    //           id="name"
    //           defaultValue={state.data.name}
    //           value={state.data.name}
    //           onChange={handleTextChange}
    //           disabled={access}
    //           required={!access}
    //         />
    //         <div className="error-message">{state.errors.name}</div>
    //       </div>
    //       <div className="form-group">
    //         <label htmlFor="owner">
    //           Owner <span style={{ color: "red" }}>*</span>:
    //         </label>
    //         <input
    //           type="text"
    //           className="form-control"
    //           name="owner"
    //           id="owner"
    //           defaultValue={state.data.owner}
    //           value={state.data.owner}
    //           onChange={e => handleTextChange(e)}
    //           disabled={access}
    //         />
    //         <div className="error-message">{state.errors.owner}</div>
    //       </div>
    //       <div className="form-group">
    //         <label htmlFor="type">Type:</label>
    //         <select
    //           className="form-control"
    //           id="type"
    //           name="type"
    //           defaultValue={state.data.type}
    //           value={state.data.type}
    //           onChange={e => handleTextChange(e)}
    //           disabled={access}
    //           required="required"
    //         >
    //           {CONSTANTS.applicationTypes.map(item => (
    //             <option key={item}>{item}</option>
    //           ))}
    //         </select>
    //       </div>
    //       <div className="form-group">
    //         <label htmlFor="type">Org:</label>
    //         <select
    //           className="form-control"
    //           id="org"
    //           name="org"
    //           defaultValue={state.data.org}
    //           value={state.data.org}
    //           onChange={e => handleTextChange(e)}
    //           disabled={access}
    //           required="required"
    //         >
    //           {orgInfo.map(item => (
    //             <option value={item.id}>{item.name}</option>
    //           ))}
    //         </select>
    //       </div>
    //       <div className="form-group">
    //         <label htmlFor="owner">Created:</label>
    //         <input
    //           type="text"
    //           className="form-control"
    //           name="createdAt"
    //           id="createdAt"
    //           defaultValue={state.data.createdAt}
    //           value={state.data.createdAt}
    //           onChange={e => handleTextChange(e)}
    //           disabled
    //         />
    //       </div>
    //       <div className="form-group">
    //         <label htmlFor="owner">Created By:</label>
    //         <input
    //           type="text"
    //           className="form-control"
    //           name="createdBy"
    //           id="createdBy"
    //           defaultValue={state.data.createdUser}
    //           value={state.data.createdUser}
    //           onChange={e => handleTextChange(e)}
    //           disabled
    //         />
    //       </div>
    //     </div>
    //   </div>
  );
};

RequestPayment.propTypes = {
  match: PropTypes.shape({
    params: PropTypes.shape({
      applicationId: PropTypes.string
    })
  }).isRequired,
  actions: PropTypes.func.isRequired
};

export default RequestPayment;
