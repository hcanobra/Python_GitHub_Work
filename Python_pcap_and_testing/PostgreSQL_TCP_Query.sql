WITH
	TABLE_NAME AS
		(
		SELECT * FROM public.pcap_tables_tcp_01272023
		ORDER BY "idx"
		),
	FRAME_DELTA AS 
		(
			SELECT 
				MIN (
					EXTRACT (EPOCH FROM (
										SELECT CAST ("l2_time" - INTERVAL '7 HOURS' AS TIME)
										)
						   )
					) 
			FROM TABLE_NAME
		),
	RELATIVE_TIME AS 
		(
			SELECT 
				"idx",

				EXTRACT (EPOCH FROM (
									SELECT CAST ("l2_time" - INTERVAL '7 HOURS' AS TIME)
									) 
						 ) - (
							   SELECT * FROM FRAME_DELTA
							 ) AS "Relative_time",

				EXTRACT
						(EPOCH FROM (
									SELECT CAST ("l2_time" - INTERVAL '7 HOURS' AS TIME)
									)
						 ) - LAG (EXTRACT (
											EPOCH FROM (
														SELECT CAST ("l2_time" - INTERVAL '7 HOURS' AS TIME)
														)
										), 1)
						OVER (
								ORDER BY EXTRACT (EPOCH FROM (
																SELECT CAST ("l2_time" - INTERVAL '7 HOURS' AS TIME)
																)
													)
							) AS "Frame_Delta",
				"TCP_seq" :: BIGINT,
				CASE 
					WHEN "TCP_flags" IN ('S','SA')
					THEN
						"l2_wirelen" - 74 
					WHEN "TCP_flags" IN ('A','PA')
					THEN
						"l2_wirelen" - 66
					END
					AS "TCP_len",
				CASE 
					WHEN "TCP_ack" :: BIGINT - 1 > 0
					THEN
						"TCP_ack" :: BIGINT
					ELSE 0
					END AS  "TCP_ack",
				"TCP_flags",
				"Frame_flow",
				"Source"
			FROM TABLE_NAME

		)

SELECT 
	*
FROM RELATIVE_TIME



