import {
  NavLink,
  Routes,
  Route
} from "react-router-dom";

import {
  LayoutDashboard,
  Users,
  Layers,
  RefreshCcw,
  AlertTriangle
} from "lucide-react";

import Dashboard from "./pages/Dashboard";
import Customers from "./pages/Customers";
import Segmentation from "./pages/Segmentation";
import Retention from "./pages/Retention";
import ChurnPrediction from "./pages/ChurnPrediction";


function App() {

  const navigation = [

    {
      path: "/",
      label: "Dashboard",
      icon: LayoutDashboard
    },

    {
      path: "/customers",
      label: "Customers",
      icon: Users
    },

    {
      path: "/segmentation",
      label: "Segmentation",
      icon: Layers
    },

    {
      path: "/retention",
      label: "Retention",
      icon: RefreshCcw
    },

    {
      path: "/churn",
      label: "Churn Prediction",
      icon: AlertTriangle
    }
  ];


  return (

    <div className="app">

      {/* ================================================== */}
      {/* SIDEBAR */}
      {/* ================================================== */}

      <aside className="sidebar">

        <div className="brand">

          <div className="brand-icon">
            CI
          </div>

          <div>

            <h1>
              Customer
            </h1>

            <span>
              Intelligence
            </span>

          </div>

        </div>


        <nav className="navigation">

          {navigation.map(
            ({
              path,
              label,
              icon: Icon
            }) => (

              <NavLink
                key={path}
                to={path}
                className={({ isActive }) =>
                  isActive
                    ? "nav-link active"
                    : "nav-link"
                }
              >

                <Icon
                  size={19}
                />

                <span>
                  {label}
                </span>

              </NavLink>

            )
          )}

        </nav>


        <div className="sidebar-footer">

          <span>
            ML Intelligence Platform
          </span>

          <small>
            v1.0.0
          </small>

        </div>

      </aside>


      {/* ================================================== */}
      {/* MAIN */}
      {/* ================================================== */}

      <main className="main-content">

        <Routes>

          <Route
            path="/"
            element={<Dashboard />}
          />

          <Route
            path="/customers"
            element={<Customers />}
          />

          <Route
            path="/segmentation"
            element={<Segmentation />}
          />

          <Route
            path="/retention"
            element={<Retention />}
          />

          <Route
            path="/churn"
            element={<ChurnPrediction />}
          />

        </Routes>

      </main>

    </div>
  );
}


export default App;