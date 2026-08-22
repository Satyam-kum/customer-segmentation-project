
import {
  useEffect,
  useState
} from "react";

import {
  RefreshCcw,
  Users
} from "lucide-react";

import StatCard from "../components/StatCard";

import {
  getRetention,
  getRetentionBySegment
} from "../services/api";


function Retention() {

  const [
    retention,
    setRetention
  ] = useState(null);

  const [
    segments,
    setSegments
  ] = useState([]);

  const [
    loading,
    setLoading
  ] = useState(true);

  const [
    error,
    setError
  ] = useState(null);


  useEffect(() => {

    async function load() {

      try {

        setLoading(true);

        setError(null);


        const [
          retentionData,
          segmentData
        ] = await Promise.all([

          getRetention(),

          getRetentionBySegment()

        ]);


        setRetention(
          retentionData
        );


        setSegments(
          Array.isArray(segmentData)
            ? segmentData
            : []
        );


      } catch (err) {

        console.error(
          "Error loading retention data:",
          err
        );


        setError(
          err?.response?.data?.detail ||
          err?.message ||
          "Unable to load retention data."
        );


      } finally {

        setLoading(false);

      }
    }


    load();

  }, []);


  /* ============================================================
     LOADING
     ============================================================ */

  if (loading) {

    return (

      <div className="loading">

        Loading retention analysis...

      </div>

    );

  }


  /* ============================================================
     ERROR
     ============================================================ */

  if (error) {

    return (

      <div className="page">

        <div className="page-header">

          <div>

            <h2>
              Retention Analysis
            </h2>

            <p>
              Understand repeat purchasing
              and customer engagement.
            </p>

          </div>

        </div>


        <div
          className="content-card"
          style={{
            padding: "24px",
            color: "#dc2626"
          }}
        >

          <h3>
            Unable to load retention data.
          </h3>

          <p>
            {error}
          </p>

          <p>
            Please make sure the FastAPI
            backend is running on port 8000
            and that the retention endpoints
            are available.
          </p>

        </div>

      </div>

    );

  }


  /* ============================================================
     SAFETY CHECK
     ============================================================ */

  if (!retention) {

    return (

      <div className="page">

        <div className="content-card">

          <h3>
            No retention data available.
          </h3>

        </div>

      </div>

    );

  }


  /* ============================================================
     MAIN PAGE
     ============================================================ */

  return (

    <div className="page">

      <div className="page-header">

        <div>

          <h2>
            Retention Analysis
          </h2>

          <p>
            Understand repeat purchasing
            and customer engagement.
          </p>

        </div>

      </div>


      {/* ======================================================
          RETENTION STATISTICS
          ====================================================== */}

      <div className="stats-grid">

        <StatCard

          title="Total Customers"

          value={
            Number(
              retention.total_customers || 0
            ).toLocaleString()
          }

          icon={Users}

        />


        <StatCard

          title="Repeat Customers"

          value={
            Number(
              retention.repeat_customers || 0
            ).toLocaleString()
          }

          icon={RefreshCcw}

        />


        <StatCard

          title="Repeat Purchase Rate"

          value={

            (
              Number(
                retention.repeat_purchase_rate || 0
              )
              * 100

            ).toFixed(1)

            + "%"

          }

          subtitle="Customers with >1 order"

        />

      </div>


      {/* ======================================================
          RETENTION BY SEGMENT
          ====================================================== */}

      <section className="content-card">

        <div className="section-header">

          <div>

            <h3>
              Retention by Segment
            </h3>

            <p>
              Compare purchasing behavior
              across customer groups.
            </p>

          </div>

        </div>


        <div className="table-wrapper">

          <table>

            <thead>

              <tr>

                <th>
                  Segment
                </th>

                <th>
                  Customers
                </th>

                <th>
                  Revenue
                </th>

                <th>
                  Avg. Frequency
                </th>

                <th>
                  Avg. Recency
                </th>

              </tr>

            </thead>


            <tbody>

              {segments.length > 0 ? (

                segments.map(
                  (segment) => (

                    <tr
                      key={
                        segment.segment
                      }
                    >

                      <td>

                        <strong>
                          {
                            segment.segment
                          }
                        </strong>

                      </td>


                      <td>

                        {Number(
                          segment.customers || 0
                        ).toLocaleString()}

                      </td>


                      <td>

                        £
                        {Math.round(
                          Number(
                            segment.revenue || 0
                          )
                        ).toLocaleString()}

                      </td>


                      <td>

                        {Number(
                          segment.average_frequency || 0
                        ).toFixed(1)}

                      </td>


                      <td>

                        {Number(
                          segment.average_recency || 0
                        ).toFixed(0)}

                        {" "}days

                      </td>

                    </tr>

                  )
                )

              ) : (

                <tr>

                  <td
                    colSpan="5"
                    style={{
                      textAlign: "center",
                      padding: "30px"
                    }}
                  >

                    No segment retention
                    data available.

                  </td>

                </tr>

              )}

            </tbody>

          </table>

        </div>

      </section>

    </div>

  );

}


export default Retention;