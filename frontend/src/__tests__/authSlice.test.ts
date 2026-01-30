import authReducer, { setCredentials, logout } from "../features/auth/authSlice";

describe("authSlice", () => {
  const initialState = {
    accessToken: null,
    refreshToken: null,
    username: null,
    userId: null,
    isAuthenticated: false,
  };

  it("should return the initial state", () => {
    expect(authReducer(undefined, { type: "unknown" })).toEqual(
      expect.objectContaining({
        isAuthenticated: false,
      })
    );
  });

  it("should handle setCredentials", () => {
    const credentials = {
      accessToken: "test-access-token",
      refreshToken: "test-refresh-token",
      username: "testuser",
      userId: "user-123",
    };

    const state = authReducer(initialState, setCredentials(credentials));

    expect(state.accessToken).toBe("test-access-token");
    expect(state.refreshToken).toBe("test-refresh-token");
    expect(state.username).toBe("testuser");
    expect(state.userId).toBe("user-123");
    expect(state.isAuthenticated).toBe(true);
  });

  it("should handle logout", () => {
    const loggedInState = {
      accessToken: "token",
      refreshToken: "refresh",
      username: "user",
      userId: "id",
      isAuthenticated: true,
    };

    const state = authReducer(loggedInState, logout());

    expect(state.accessToken).toBeNull();
    expect(state.refreshToken).toBeNull();
    expect(state.username).toBeNull();
    expect(state.userId).toBeNull();
    expect(state.isAuthenticated).toBe(false);
  });
});
