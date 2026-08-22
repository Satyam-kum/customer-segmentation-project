import {
  useEffect,
  useState
} from "react";

import {
  AlertTriangle,
  Search
} from "lucide-react";

import {
  getCustomerChurn,
  getHighRiskCustomers
} from "../services/api";


function ChurnPrediction() {

  const [
    customerId,
    setCustomerId
  ] = useState("");

  const [
    prediction,
    setPrediction
  ] = useState(null);

  const [
    highRisk,
    setHighRisk
  ] = useState([]);

  const [
    loading,
    setLoading
  ] = useState(false);


  useEffect(() => {

    async function loadHighRisk() {

      try {

        const data =
          await getHighRiskCustomers(
            20
          );

        setHighRisk(
          data
        );

      } catch (error) {

        console.error(error);

      }
    }

    loadHighRisk();

  }, []);


  async function predict(
    event
  ) {

    event.preventDefault();

    if (!customerId.trim()) {

      return;
    }

    try {

      setLoading(true);

      const data =
        await getCustomerChurn(
          customerId.trim()
        );

      setPrediction(
        data
      );

    } catch (error) {

      setPrediction({
        error:
          error.response?.data
            ?.detail ||
          "Unable to predict churn."
      });

    } finally {

      setLoading(false);

    }
  }


  return (

    <div className="page">

      <div className="page-header">

        <div>

          <h2>
            Churn Prediction
          </h2>

          <p>
            Identify customers at risk
            of becoming inactive.
          </p>

        </div>

      </div>


      <section className="content-card">

        <div className="section-header">

          <div>

            <h3>
              Predict Customer Churn
            </h3>

            <p>
              Enter a customer ID to
              calculate churn probability.
            </p>

          </div>

        </div>


        <form
          className="search-bar"
          onSubmit={predict}
        >

          <Search
            size={19}
          />

          <input

            value={customerId}

            onChange={(event) =>
              setCustomerId(
                event.target.value
              )
            }

            placeholder="Enter Customer ID"

          />

          <button
            className="primary-button"
            type="submit"
          >

            {loading
              ? "Predicting..."
              : "Predict Churn"}

          </button>

        </form>


        {prediction &&
          !prediction.error && (

            <div className="prediction-result">

              <div>

                <span>
                  Customer
                </span>

                <strong>
                  #{prediction.customer_id}
                </strong>

              </div>


              <div>

                <span>
                  Churn Probability
                </span>

                <strong>
                  {
                    (
                      prediction
                        .churn_probability
                      * 100
                    ).toFixed(1)
                  }%
                </strong>

              </div>


              <div>

                <span>
                  Risk
                </span>

                <strong
                  className={
                    `risk-${prediction.risk.toLowerCase()}`
                  }
                >
                  {prediction.risk}
                </strong>

              </div>


              <div>

                <span>
                  Recommended Action
                </span>

                <strong>
                  {
                    prediction
                      .retention_action
                  }
                </strong>

              </div>

            </div>

          )}


        {prediction?.error && (

          <div className="error-box">
            {prediction.error}
          </div>

        )}

      </section>


      <section className="content-card">

        <div className="section-header">

          <div>

            <h3>
              High-Risk Customers
            </h3>

            <p>
              Customers requiring
              retention attention.
            </p>

          </div>

          <AlertTriangle
            size={22}
          />

        </div>


        <div className="table-wrapper">

          <table>

            <thead>

              <tr>

                <th>
                  Customer
                </th>

                <th>
                  Probability
                </th>

                <th>
                  Risk
                </th>

                <th>
                  Recommended Action
                </th>

              </tr>

            </thead>


            <tbody>

              {highRisk.map(
                (customer) => (

                  <tr
                    key={
                      customer.customer_id
                    }
                  >

                    <td>
                      #{customer.customer_id}
                    </td>

                    <td>

                      {
                        (
                          customer
                            .churn_probability
                          * 100
                        ).toFixed(1)
                      }%

                    </td>

                    <td>

                      <span
                        className="risk-high"
                      >
                        HIGH
                      </span>

                    </td>

                    <td>
                      {
                        customer
                          .retention_action
                      }
                    </td>

                  </tr>

                )
              )}

            </tbody>

          </table>

        </div>

      </section>

    </div>
  );
}


export default ChurnPrediction;