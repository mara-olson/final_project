// import Card from "/static/Components/Card";
const { Route, BrowserRouter } = ReactRouterDOM;

function App() {
  const [userId, setUserId] = React.useState(null);
  const [isLoggedIn, setIsLoggedIn] = React.useState(false);
  const [error, setError] = React.useState(null);

  React.useEffect(() => {
    const isLoggedIn = localStorage.getItem("isLoggedIn");
    if (isLoggedIn) {
      setIsLoggedIn(JSON.parse(isLoggedIn));
    }
  }, []);

  React.useEffect(() => {
    const userId = localStorage.getItem("userId");
    if (userId) {
      setUserId(JSON.parse(userId));
    }
  }, []);

  return (
    <BrowserRouter>
      <Navbar
        logo="/static/period-logo.png"
        userId={userId}
        setUserId={setUserId}
        setIsLoggedIn={setIsLoggedIn}
        isLoggedIn={isLoggedIn}
      />
      {error && <p className="error">{error}</p>}
      {!isLoggedIn && (
        <div className="container-fluid">
          <Route exact path="/">
            <LandingPage />
          </Route>
        </div>
      )}
      <div className="container-fluid">
        <Route exact path="/login">
          <Login
            userId={userId}
            setUserId={setUserId}
            setIsLoggedIn={setIsLoggedIn}
            setError={setError}
          />
        </Route>
      </div>
      <div className="container-fluid">
        <Route exact path="/users/:user_id/home">
          <Home userId={userId} />
        </Route>
      </div>
      <div className="container-fluid">
        <Route exact path="/users/:user_id/activities">
          <ActivitiesContainer userId={userId} />
          <AddActivityButton userId={userId} />
        </Route>
      </div>
      <div className="container-fluid">
        <Route exact path="/users/:user_id/profile">
          <Profile userId={userId} />
        </Route>
      </div>
      <div className="container-fluid">
        <Route exact path="/sign-up">
          <SignUp setUserId={setUserId} />
        </Route>
      </div>

      {/* {Route path = '*' /* cutsie catch-all error page default if no route found */}
    </BrowserRouter>
  );
}

ReactDOM.render(<App />, document.querySelector("#root"));
