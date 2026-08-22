import {
  useEffect,
  useState
} from "react";

import {
  getSegmentSummary
} from "../services/api";


function formatCurrency(
  value
) {

  return new Intl.NumberFormat(
    "en-IN",
    {
      style: "currency",
      currency: "GBP",
      maximumFractionDigits: 0
    }
  ).format(
    value || 0
  );
}


function Segmentation() {

  const [
    segments,
    setSegments
  ] = useState([]);

  const [
    loading,
    setLoading
  ] = useState(true);


  useEffect(() => {

    async function load() {

      try {

        const data =
          await getSegmentSummary();

        setSegments(
          data
        );

      } finally {

        setLoading(false);

      }
    }

    load();

  }, []);


  return (

    <div className="page">

      <div className="page-header">

        <div>

          <h2>
            Customer Segmentation
          </h2>

          <p>
            RFM-based customer clusters
            generated using machine learning.
          </p>

        </div>

      </div>


      {loading ? (

        <div className="loading">
          Loading segments...
        </div>

      ) : (

        <div className="segment-grid">

          {segments.map(
            (segment) => (

              <div
                className="segment-card"
                key={
                  segment.cluster
                }
              >

                <div className="segment-number">

                  Cluster {
                    segment.cluster
                  }

                </div>


                <h3>
                  {segment.segment}
                </h3>


                <div className="segment-stat">

                  <span>
                    Customers
                  </span>

                  <strong>
                    {
                      segment.customers
                        .toLocaleString()
                    }
                  </strong>

                </div>


                <div className="segment-stat">

                  <span>
                    Revenue
                  </span>

                  <strong>
                    {
                      formatCurrency(
                        segment.revenue
                      )
                    }
                  </strong>

                </div>


                <div className="segment-stat">

                  <span>
                    Avg. Frequency
                  </span>

                  <strong>
                    {
                      segment.average_frequency
                        .toFixed(1)
                    }
                  </strong>

                </div>


                <div className="segment-stat">

                  <span>
                    Avg. Recency
                  </span>

                  <strong>
                    {
                      segment.average_recency
                        .toFixed(0)
                    } days
                  </strong>

                </div>

              </div>

            )
          )}

        </div>

      )}

    </div>
  );
}


export default Segmentation;