import {
  ApolloClient,
  gql,
  LazyQueryHookOptions,
  MutationHookOptions,
  MutationOptions,
  NormalizedCacheObject,
  QueryHookOptions,
  QueryOptions,
  SubscriptionHookOptions,
  SubscriptionOptions,
  useLazyQuery,
  useMutation,
  useQuery,
  useSubscription,
} from "@apollo/client";

import { useState, useEffect } from "react";

import {
  $,
  MapType,
  mutation_root,
  query_root,
  subscription_root,
  ValueTypes,
  Zeus,
} from "./generated/graphql-client-sdk";

export { $ as $ };

export function useFetchedQuery(endpoint: string, naturalQuery: string, queryFilters: Record<string, any>) {
  const [result, setResult] = useState({ loading: true, error: null, data: null });

  useEffect(() => {
    const fetchData = async () => {
      if (!naturalQuery) {
        setResult({
          loading: false,
          error: new Error("The 'naturalQuery' cannot be null or empty."),
          data: null
        });
        return;
      }

      try {
        const response = await fetch(endpoint, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ natural_query: naturalQuery ,
          query_filters: queryFilters
          }),
        });

        if (!response.ok) {
          const text = await response.text();
          throw new Error(`HTTP error! Status: ${response.status}, Body: ${text}`);
        }

        const data = await response.json();
        setResult({ loading: false, error: null, data });
      } catch (error) {
        setResult({ loading: false, error, data: null });
      }
    };

    fetchData();
  }, [endpoint, naturalQuery]);

  return result;
}


export function useTypedQuery<Q extends ValueTypes["query_root"]>(
  query: Q,
  options?: QueryHookOptions<MapType<query_root, Q>, Record<string, any>>
) {
  return useQuery<MapType<query_root, Q>>(gql(Zeus.query(query)), options);
}

export function useTypedLazyQuery<Q extends ValueTypes["query_root"]>(
  query: Q,
  options?: LazyQueryHookOptions<MapType<query_root, Q>, Record<string, any>>
) {
  return useLazyQuery<MapType<query_root, Q>>(gql(Zeus.query(query)), options);
}

export function useTypedMutation<Q extends ValueTypes["mutation_root"]>(
  mutation: Q,
  options?: MutationHookOptions<MapType<mutation_root, Q>, Record<string, any>>
) {
  return useMutation<MapType<mutation_root, Q>>(
    gql(Zeus.mutation(mutation)),
    options
  );
}

export function useTypedSubscription<Q extends ValueTypes["subscription_root"]>(
  subscription: Q,
  options?: SubscriptionHookOptions<
    MapType<subscription_root, Q>,
    Record<string, any>
  >
) {
  return useSubscription<MapType<subscription_root, Q>>(
    gql(Zeus.subscription(subscription)),
    options
  );
}

///////////////////////////////////////////////
// These functions allow to use the Apollo client
// instance currently constructed/available in-context
// for making type-inferenced queries

export function useTypedClientQuery<Q extends ValueTypes["query_root"]>(
  apollo: ApolloClient<NormalizedCacheObject>,
  query: Q,
  options?: QueryOptions<MapType<query_root, Q>, Record<string, any>>
) {
  return apollo.query<MapType<query_root, Q>>({
    query: gql(Zeus.query(query)),
    ...options,
  });
}

export function useTypedClientMutation<Q extends ValueTypes["mutation_root"]>(
  apollo: ApolloClient<NormalizedCacheObject>,
  mutation: Q,
  options?: MutationOptions<MapType<mutation_root, Q>, Record<string, any>>
) {
  return apollo.mutate<MapType<mutation_root, Q>>({
    mutation: gql(Zeus.mutation(mutation)),
    ...options,
  });
}

function useTypedClientSubscription<Q extends ValueTypes["subscription_root"]>(
  apollo: ApolloClient<NormalizedCacheObject>,
  subscription: Q,
  options?: SubscriptionOptions<
    MapType<subscription_root, Q>,
    Record<string, any>
  >
) {
  return apollo.subscribe<MapType<subscription_root, Q>>({
    query: gql(Zeus.subscription(subscription)),
    ...options,
  });
}
