  SELECT
    #count(*) as numberOfProject,
    t0.contributors,
    t2.repo_name,
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
        UNNEST(LANGUAGE) arr 
        WHERE arr.name ="Scala") AS t1 ) AS t2
    JOIN(SELECT
              repo_name[OFFSET(0)] as repo_name,
              ARRAY_LENGTH(ARRAY_AGG(DISTINCT author.email)) as contributors
            FROM
              `bigquery-public-data.github_repos.commits`
            GROUP BY repo_name
            ) t0 on t0.repo_name=t2.repo_name
  WHERE
    rank = 1 
GROUP BY t2.LANGUAGE, t2.repo_name, t0.contributors
order by t0.contributors desc

#query per estrarre oltre che repo e linguaggio il numero di contributors