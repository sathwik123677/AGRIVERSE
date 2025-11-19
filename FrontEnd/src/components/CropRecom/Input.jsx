import React, { useState } from "react";

export default function Input(props) {
  // Initialize state for the required attribute
  const [isRequired, setIsRequired] = useState(props.required === "yes");

  return (
    <>
      <div className="mb-4">
        <label
          className="block text-gray-700 text-sm font-bold mb-2"
          htmlFor={props.htmlfor}
        >
          {props.label}
        </label>
        <input
          className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline focus:ring-0 focus:border-gray-900 placeholder-[#a56d39]"
          id="temperature"
          type={props.type}
          placeholder={props.placeholder}
          onChange={props.handleChange}
          required={true && props.required=="yes"}
        />
      </div>
    </>
  );
}
