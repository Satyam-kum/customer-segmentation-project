// import {
//   useEffect,
//   useState
// } from "react";

// import {
//   Users,
//   ShoppingCart,
//   PoundSterling,
//   AlertTriangle
// } from "lucide-react";

// import StatCard from "../components/StatCard";

// import RevenueChart from "../charts/RevenueChart";

// import SegmentChart from "../charts/SegmentChart";

// import {
//   getDashboard,
//   getRevenue,
//   getSegmentDistribution,
//   getTopCustomers
// } from "../services/api";

// import CustomerTable from "../components/CustomerTable";


// function formatCurrency(
//   value
// ) {

//   return new Intl.NumberFormat(
//     "en-IN",
//     {
//       style: "currency",
//       currency: "GBP",
//       maximumFractionDigits: 0
//     }
//   ).format(
//     value || 0
//   );
// }


// function Dashboard() {

//   const [
//     dashboard,
//     setDashboard
//   ] = useState(null);

//   const [
//     revenue,
//     setRevenue
//   ] = useState([]);

//   const [
//     segments,
//     setSegments
//   ] = useState([]);

//   const [
//     topCustomers,
//     setTopCustomers
//   ] = useState([]);

//   const [
//     loading,
//     setLoading
//   ] = useState(true);

//   const [
//     error,
//     setError
//   ] = useState("");


//   useEffect(() => {

//     async function loadData() {

//       try {

//         setLoading(true);

//         const [
//           dashboardData,
//           revenueData,
//           segmentData,
//           customerData
//         ] = await Promise.all([

//           getDashboard(),

//           getRevenue(),

//           getSegmentDistribution(),

//           getTopCustomers(8)

//         ]);

//         setDashboard(
//           dashboardData
//         );

//         setRevenue(
//           revenueData
//         );

//         setSegments(
//           segmentData
//         );

//         setTopCustomers(
//           customerData
//         );

//       } catch (err) {

//         console.error(err);

//         setError(
//           "Unable to load dashboard data."
//         );

//       } finally {

//         setLoading(false);

//       }
//     }

//     loadData();

//   }, []);


//   if (loading) {

//     return (
//       <div className="loading">
//         Loading dashboard...
//       </div>
//     );
//   }


//   if (error) {

//     return (
//       <div className="error-box">
//         {error}
//       </div>
//     );
//   }


//   return (

//     <div className="page">

//       <div className="page-header">

//         <div>

//           <h2>
//             Customer Intelligence Dashboard
//           </h2>

//           <p>
//             Monitor customer value, engagement,
//             retention and churn risk.
//           </p>

//         </div>

//       </div>


//       <div className="stats-grid">

//         <StatCard

//           title="Total Customers"

//           value={
//             dashboard.total_customers
//               .toLocaleString()
//           }

//           subtitle="Unique customers"

//           icon={Users}

//         />


//         <StatCard

//           title="Total Orders"

//           value={
//             dashboard.total_orders
//               .toLocaleString()
//           }

//           subtitle="Unique invoices"

//           icon={ShoppingCart}

//         />


//         <StatCard

//           title="Total Revenue"

//           value={
//             formatCurrency(
//               dashboard.total_revenue
//             )
//           }

//           subtitle="Historical revenue"

//           icon={PoundSterling}

//         />


//         <StatCard

//           title="Revenue at Risk"

//           value={
//             formatCurrency(
//               dashboard.revenue_at_risk
//             )
//           }

//           subtitle={
//             `${dashboard.high_risk_customers} high-risk customers`
//           }

//           icon={AlertTriangle}

//         />

//       </div>


//       <div className="charts-grid">

//         <RevenueChart
//           data={revenue}
//         />

//         <SegmentChart
//           data={segments}
//         />

//       </div>


//       <section className="content-card">

//         <div className="section-header">

//           <div>

//             <h3>
//               Top Customers
//             </h3>

//             <p>
//               Highest-value customers by revenue
//             </p>

//           </div>

//         </div>


//         <CustomerTable
//           customers={
//             topCustomers
//           }
//         />

//       </section>

//     </div>
//   );
// }


// export default Dashboard;

import { useEffect, useState } from "react";

import {
  Users,
  ShoppingCart,
  PoundSterling,
  AlertTriangle,
} from "lucide-react";

import StatCard from "../components/StatCard";

import RevenueChart from "../charts/RevenueChart";
import SegmentChart from "../charts/SegmentChart";

import {
  getDashboard,
  getRevenue,
  getSegmentDistribution,
  getTopCustomers,
} from "../services/api";

import CustomerTable from "../components/CustomerTable";


/* ============================================================
   FORMAT CURRENCY
   ============================================================ */

function formatCurrency(value) {
  const number = Number(value) || 0;

  return new Intl.NumberFormat("en-IN", {
    style: "currency",
    currency: "GBP",
    maximumFractionDigits: 0,
  }).format(number);
}


/* ============================================================
   DASHBOARD COMPONENT
   ============================================================ */

function Dashboard() {
  const [dashboard, setDashboard] = useState(null);

  const [revenue, setRevenue] = useState([]);

  const [segments, setSegments] = useState([]);

  const [topCustomers, setTopCustomers] = useState([]);

  const [loading, setLoading] = useState(true);

  const [error, setError] = useState("");


  /* ==========================================================
     LOAD DASHBOARD DATA
     ========================================================== */

  useEffect(() => {
    let mounted = true;

    async function loadData() {
      try {
        setLoading(true);
        setError("");

        console.log("====================================");
        console.log("Loading dashboard data...");
        console.log("====================================");


        /* ----------------------------------------------------
           Run all API calls independently
           ---------------------------------------------------- */

        const results = await Promise.allSettled([
          getDashboard(),
          getRevenue(),
          getSegmentDistribution(),
          getTopCustomers(8),
        ]);


        const [
          dashboardResult,
          revenueResult,
          segmentResult,
          customerResult,
        ] = results;


        /* ----------------------------------------------------
           DASHBOARD
           ---------------------------------------------------- */

        if (dashboardResult.status === "fulfilled") {
          console.log(
            "Dashboard API:",
            dashboardResult.value
          );

          if (mounted) {
            setDashboard(
              dashboardResult.value
            );
          }
        } else {
          console.error(
            "Dashboard API failed:",
            dashboardResult.reason
          );
        }


        /* ----------------------------------------------------
           REVENUE
           ---------------------------------------------------- */

        if (revenueResult.status === "fulfilled") {
          console.log(
            "Revenue API:",
            revenueResult.value
          );

          if (mounted) {
            setRevenue(
              Array.isArray(revenueResult.value)
                ? revenueResult.value
                : []
            );
          }
        } else {
          console.error(
            "Revenue API failed:",
            revenueResult.reason
          );
        }


        /* ----------------------------------------------------
           SEGMENTS
           ---------------------------------------------------- */

        if (segmentResult.status === "fulfilled") {
          console.log(
            "Segment API:",
            segmentResult.value
          );

          if (mounted) {
            setSegments(
              Array.isArray(segmentResult.value)
                ? segmentResult.value
                : []
            );
          }
        } else {
          console.error(
            "Segment API failed:",
            segmentResult.reason
          );
        }


        /* ----------------------------------------------------
           TOP CUSTOMERS
           ---------------------------------------------------- */

        if (customerResult.status === "fulfilled") {
          console.log(
            "Top Customers API:",
            customerResult.value
          );

          if (mounted) {
            setTopCustomers(
              Array.isArray(customerResult.value)
                ? customerResult.value
                : []
            );
          }
        } else {
          console.error(
            "Top Customers API failed:",
            customerResult.reason
          );
        }


        /* ----------------------------------------------------
           FIND FAILED REQUESTS
           ---------------------------------------------------- */

        const failedRequests = results
          .map((result, index) => {
            if (result.status === "rejected") {
              const names = [
                "getDashboard",
                "getRevenue",
                "getSegmentDistribution",
                "getTopCustomers",
              ];

              return names[index];
            }

            return null;
          })
          .filter(Boolean);


        if (failedRequests.length > 0) {
          console.error(
            "Failed API requests:",
            failedRequests
          );

          if (mounted) {
            setError(
              `Some dashboard data could not be loaded: ${failedRequests.join(
                ", "
              )}`
            );
          }
        }


      } catch (err) {
        console.error(
          "Unexpected dashboard error:",
          err
        );

        if (mounted) {
          setError(
            "Unable to load dashboard data."
          );
        }

      } finally {
        if (mounted) {
          setLoading(false);
        }
      }
    }


    loadData();


    return () => {
      mounted = false;
    };

  }, []);


  /* ==========================================================
     LOADING
     ========================================================== */

  if (loading) {
    return (
      <div className="loading">
        Loading dashboard...
      </div>
    );
  }


  /* ==========================================================
     COMPLETE API FAILURE
     ========================================================== */

  if (!dashboard && error) {
    return (
      <div className="page">

        <div className="error-box">

          <strong>
            Unable to load dashboard data.
          </strong>

          <p>
            {error}
          </p>

          <p>
            Please check that the FastAPI backend is
            running on port 8000 and that the API
            endpoints are available.
          </p>

        </div>

      </div>
    );
  }


  /* ==========================================================
     DASHBOARD DATA FALLBACK
     ========================================================== */

  const safeDashboard = dashboard || {
    total_customers: 0,
    total_orders: 0,
    total_revenue: 0,
    revenue_at_risk: 0,
    high_risk_customers: 0,
  };


  /* ==========================================================
     RENDER
     ========================================================== */

  return (
    <div className="page">


      {/* ======================================================
          ERROR WARNING
          ====================================================== */}

      {error && (
        <div className="error-box">
          {error}
        </div>
      )}


      {/* ======================================================
          PAGE HEADER
          ====================================================== */}

      <div className="page-header">

        <div>

          <h2>
            Customer Intelligence Dashboard
          </h2>

          <p>
            Monitor customer value, engagement,
            retention and churn risk.
          </p>

        </div>

      </div>


      {/* ======================================================
          STAT CARDS
          ====================================================== */}

      <div className="stats-grid">


        {/* TOTAL CUSTOMERS */}

        <StatCard
          title="Total Customers"

          value={
            Number(
              safeDashboard.total_customers
            ).toLocaleString()
          }

          subtitle="Unique customers"

          icon={Users}
        />


        {/* TOTAL ORDERS */}

        <StatCard
          title="Total Orders"

          value={
            Number(
              safeDashboard.total_orders
            ).toLocaleString()
          }

          subtitle="Unique invoices"

          icon={ShoppingCart}
        />


        {/* TOTAL REVENUE */}

        <StatCard
          title="Total Revenue"

          value={
            formatCurrency(
              safeDashboard.total_revenue
            )
          }

          subtitle="Historical revenue"

          icon={PoundSterling}
        />


        {/* REVENUE AT RISK */}

        <StatCard
          title="Revenue at Risk"

          value={
            formatCurrency(
              safeDashboard.revenue_at_risk
            )
          }

          subtitle={
            `${
              Number(
                safeDashboard.high_risk_customers
              )
            } high-risk customers`
          }

          icon={AlertTriangle}
        />

      </div>


      {/* ======================================================
          CHARTS
          ====================================================== */}

      <div className="charts-grid">

        <RevenueChart
          data={revenue}
        />

        <SegmentChart
          data={segments}
        />

      </div>


      {/* ======================================================
          TOP CUSTOMERS
          ====================================================== */}

      <section className="content-card">

        <div className="section-header">

          <div>

            <h3>
              Top Customers
            </h3>

            <p>
              Highest-value customers by revenue
            </p>

          </div>

        </div>


        <CustomerTable
          customers={topCustomers}
        />

      </section>

    </div>
  );
}


export default Dashboard;