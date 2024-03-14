"use client";

import useSWR from "swr";

const fetcher = (...args: any[]) => fetch(...args).then((res) => res.json());


export default function EntityDetailPage({params}) {
  const {entity_id} = params
  const url = `http://localhost:8000/api/entities/${entity_id}`;
  const { data, error, isLoading } = useSWR(url, fetcher);
  if (error) return <div>failed to load</div>;
  if (isLoading) return <div>loading...</div>;

  return <div> {JSON.stringify(data)} </div>;
}
