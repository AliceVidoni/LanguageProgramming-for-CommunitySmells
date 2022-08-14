  SELECT
    count(*) as numberOfProject,
    #t2.repo_name,
    t2.LANGUAGE
  FROM (
    SELECT
      repo_name,
      LANGUAGE,
      RANK() OVER (PARTITION BY t1.repo_name ORDER BY t1.language_bytes DESC) AS rank
    FROM (
      SELECT
        repo_name,
        arr.name AS LANGUAGE,
        arr.bytes AS language_bytes
      FROM
        `bigquery-public-data.github_repos.languages`,
        UNNEST(LANGUAGE) arr ) AS t1 ) AS t2
  WHERE
    rank = 1 
GROUP BY t2.LANGUAGE

#query per ottenere numero di repo per ogni linguaggio