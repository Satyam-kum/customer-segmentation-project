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


function CustomerTable({
  customers = [],
  onCustomerClick
}) {

  return (

    <div className="table-wrapper">

      <table>

        <thead>

          <tr>

            <th>
              Customer
            </th>

            <th>
              Segment
            </th>

            <th>
              Recency
            </th>

            <th>
              Orders
            </th>

            <th>
              Revenue
            </th>

          </tr>

        </thead>


        <tbody>

          {customers.map(
            (customer) => (

              <tr
                key={
                  customer.customer_id
                }
                onClick={() =>
                  onCustomerClick &&
                  onCustomerClick(
                    customer
                  )
                }
              >

                <td>

                  <button
                    className="customer-link"
                    onClick={(event) => {
                      event.stopPropagation();

                      onCustomerClick &&
                        onCustomerClick(
                          customer
                        );
                    }}
                  >

                    #{customer.customer_id}

                  </button>

                </td>


                <td>

                  <span
                    className="segment-badge"
                  >
                    {customer.segment ||
                      "Unassigned"}
                  </span>

                </td>


                <td>
                  {Math.round(
                    customer.recency || 0
                  )} days
                </td>


                <td>
                  {Math.round(
                    customer.frequency || 0
                  )}
                </td>


                <td>
                  {formatCurrency(
                    customer.monetary
                  )}
                </td>

              </tr>

            )
          )}

        </tbody>

      </table>


      {!customers.length && (

        <div className="empty-state">
          No customers found.
        </div>

      )}

    </div>
  );
}


export default CustomerTable;