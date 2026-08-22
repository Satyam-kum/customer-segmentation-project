import {
  useEffect,
  useState
} from "react";

import {
  Search
} from "lucide-react";

import CustomerTable from "../components/CustomerTable";

import {
  getCustomers
} from "../services/api";


function Customers() {

  const [
    customers,
    setCustomers
  ] = useState([]);

  const [
    total,
    setTotal
  ] = useState(0);

  const [
    page,
    setPage
  ] = useState(1);

  const [
    search,
    setSearch
  ] = useState("");

  const [
    loading,
    setLoading
  ] = useState(false);


  const pageSize = 20;


  async function loadCustomers() {

    try {

      setLoading(true);

      const data =
        await getCustomers({

          page,

          pageSize,

          search

        });

      setCustomers(
        data.customers
      );

      setTotal(
        data.total
      );

    } finally {

      setLoading(false);

    }
  }


  useEffect(() => {

    loadCustomers();

  }, [page]);


  function handleSearch(
    event
  ) {

    event.preventDefault();

    setPage(1);

    loadCustomers();

  }


  const totalPages =
    Math.ceil(
      total / pageSize
    );


  return (

    <div className="page">

      <div className="page-header">

        <div>

          <h2>
            Customers
          </h2>

          <p>
            Explore customer behavior,
            value and segmentation.
          </p>

        </div>

      </div>


      <div className="content-card">

        <form
          className="search-bar"
          onSubmit={handleSearch}
        >

          <Search
            size={19}
          />

          <input

            value={search}

            onChange={(event) =>
              setSearch(
                event.target.value
              )
            }

            placeholder="Search customer ID..."

          />

          <button
            type="submit"
            className="primary-button"
          >
            Search
          </button>

        </form>


        {loading ? (

          <div className="loading">
            Loading customers...
          </div>

        ) : (

          <CustomerTable
            customers={
              customers
            }
          />

        )}


        <div className="pagination">

          <button

            disabled={
              page <= 1
            }

            onClick={() =>
              setPage(
                page - 1
              )
            }

          >
            Previous
          </button>


          <span>

            Page {page} of {
              Math.max(
                totalPages,
                1
              )
            }

          </span>


          <button

            disabled={
              page >= totalPages
            }

            onClick={() =>
              setPage(
                page + 1
              )
            }

          >
            Next
          </button>

        </div>

      </div>

    </div>
  );
}


export default Customers;