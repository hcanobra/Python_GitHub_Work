WITH
	TABLE_NAME AS
		(
		SELECT * FROM public.pcap_tables_tcp_retransmition_02132023
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
				"l2_time",

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

				"Time_since_previous",
				"src",
				"dst",
				"srcport",
				"dstport",
				"rel_ack",
				"raw_ack",
				"rel_seq",
				"raw_seq",
				"TCP_Flag",
				"Analysis"
			FROM TABLE_NAME

		)

SELECT 
	*
FROM RELATIVE_TIME