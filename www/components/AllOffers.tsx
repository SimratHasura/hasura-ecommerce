import React, { useState, useEffect } from 'react';
import { useAtom } from "jotai";
import Link from "next/link";
import { useRouter } from "next/router";
import { searchState } from "../state/FilterState";
import { useFetchedQuery } from "../utils/gql-zeus-query-hooks";
import Offer from "./Offer";

const AllOffers = () => {
  const [search] = useAtom(searchState);
  const router = useRouter();

  const page: number = Number(router.query.page) || 1;
  const numItemsPerPage: number = Number(router.query.numItemsPerPage) || 12;
  const naturalQuery = search.searchString; // Assuming 'search' holds the natural query string
  console.log("naturalQuery: "+ naturalQuery)
  fetch(`${process.env.NEXT_PUBLIC_HASURA_SUPERRAG_CLIENTSIDE}/hello_world`)
  .then(response => {
    if (!response.ok) {
      throw new Error(`[HelloWorld]: HTTP error! status: ${response.status}`);
    }
    return response.json();
  })
  .then(data => {
    console.log('[HelloWorld]: Data:', data);
  })
  .catch(error => {
    console.error('[HelloWorld]: Fetch error:', error.message);
  });



  const superrag_server = process.env.NEXT_PUBLIC_HASURA_SUPERRAG_CLIENTSIDE;
  const superrag_endpoint = superrag_server + "/query_product"


  // Function to navigate to a different page
  function goToPage(newPage: number) {
    router.push({ pathname: "./", query: { page: newPage } });
  }

  // // New state for loading and error management
  // const [loading, setLoading] = useState(false);
  // const [error, setError] = useState(null);

  const queryFilters = {
    category: search.category_display_name
  }

  // Fetching the query
  const { loading, error, data } = useFetchedQuery(superrag_endpoint, naturalQuery, queryFilters);
  console.log("Complete search object", search)
  console.log("Search value", search.searchString)
  console.log("Response from SuperRAG server")
  console.log(loading)
  console.log(error)
  console.log(data)

  return (
    <div className="container">
      <h2>Best Sellers</h2>
      <p className="mb-md muted">Best sellers from around the web.</p>
      <div className="shadow card mb-md">
        <div className="flex offers">
          {loading && <p>Loading...</p>}
          {error && <p>Error: {error.message}</p>}
          {data?.product?.map((product, index) => (
            <Link key={index} href={`/products/${product.id}`}>
              <a className="flex-col border offer col-3 pad-md">
                <Offer product={product} rating={3} reviews={"1,100"} />
              </a>
            </Link>
          ))}
        </div>
      </div>
    </div>
  );
};

export default AllOffers;
