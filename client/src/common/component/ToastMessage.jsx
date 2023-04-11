import React from "react";
import PropTypes from "prop-types";
import { utils } from "../utils";

export const CreatedSuccessToastMessage = ({
  object,
  recordName,
  linkPath
}) => {
  return (
    <p>
      {utils.capitalizeFirstLetter(object)}{" "}
      {utils.truncateRecordName(recordName)} successfully created.{" "}
      <a href={linkPath}>Go to this {utils.uncapitalizeFirstLetter(object)}</a>
    </p>
  );
};

export const CreatedErrorToastMessage = ({ object, recordName }) => {
  return (
    <p>
      {utils.capitalizeFirstLetter(object)}{" "}
      {utils.truncateRecordName(recordName)} creation failed.
    </p>
  );
};

export const UpdatedSuccessToastMessage = ({ object, recordName }) => {
  return (
    <p>
      {utils.capitalizeFirstLetter(object)}{" "}
      {utils.truncateRecordName(recordName)} updated successfully.
    </p>
  );
};

export const DeletedSuccessToastMessage = ({ object, recordName }) => {
  return (
    <p>
      {utils.capitalizeFirstLetter(object)}{" "}
      {utils.truncateRecordName(recordName)} deleted successfully.
    </p>
  );
};

export const PlainToastMessage = ({ message }) => {
  return <p>{message}</p>;
};

CreatedSuccessToastMessage.propTypes = {
  object: PropTypes.string.isRequired,
  recordName: PropTypes.string.isRequired,
  linkPath: PropTypes.string.isRequired
};

CreatedErrorToastMessage.propTypes = {
  object: PropTypes.string.isRequired,
  recordName: PropTypes.string.isRequired
};

UpdatedSuccessToastMessage.propTypes = {
  object: PropTypes.string.isRequired,
  recordName: PropTypes.string.isRequired
};

DeletedSuccessToastMessage.propTypes = {
  object: PropTypes.string.isRequired,
  recordName: PropTypes.string.isRequired
};

PlainToastMessage.propTypes = {
  message: PropTypes.string.isRequired
};
