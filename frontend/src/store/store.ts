import { createSlice, configureStore } from "@reduxjs/toolkit";

const initialState = {
  first_name: null,
  last_name: null,
  user_id: null,
  token: null,
  email: null,
};

export type AuthState = {
  first_name: string, 
  last_name: string, 
  user_id: string, 
  token: string, 
  email: string
}

const authSlice = createSlice({
  name: "auth",
  initialState,
  reducers: {
    setFirstName: (state, action) => {
      state.first_name = action.payload.first_name;
    },
    setLastName: (state, action) => {
      state.last_name = action.payload.last_name;
    },
    setUserId: (state, action) => {
      state.user_id = action.payload.user_id;
    },
    setToken: (state, action) => {
      state.token = action.payload.token;
    },
    setEmail: (state, action) => {
      state.email = action.payload.email;
    },
  },
});

const store = configureStore({
  reducer: authSlice.reducer,
});

export const authActions = authSlice.actions;
export default store;
