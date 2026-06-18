"""
Care Transition Efficiency & Placement Outcome Analytics
UAC Program Dashboard — ShadowFox AIML Internship
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
from io import StringIO

# ─────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="UAC Care Transition Analytics",
    page_icon="🏛️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─────────────────────────────────────────────
# CUSTOM CSS
# ─────────────────────────────────────────────
st.markdown("""
<style>
    /* Main palette */
    :root {
        --navy:   #0D1B2A;
        --steel:  #1B3A5C;
        --accent: #2E86AB;
        --teal:   #3BCEAC;
        --amber:  #E8A838;
        --red:    #D64045;
        --text:   #E8EDF2;
        --muted:  #8FA5BA;
        --card:   #1A2F47;
    }

    .stApp { background: #0D1B2A; color: #E8EDF2; }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background: #122236 !important;
        border-right: 1px solid #1B3A5C;
    }
    section[data-testid="stSidebar"] * { color: #E8EDF2 !important; }

    /* KPI cards */
    .kpi-card {
        background: #1A2F47;
        border: 1px solid #1B3A5C;
        border-radius: 10px;
        padding: 1.1rem 1.4rem;
        text-align: center;
        border-top: 3px solid #2E86AB;
    }
    .kpi-label  { font-size: 0.72rem; color: #8FA5BA; letter-spacing: .06em; text-transform: uppercase; margin-bottom: 6px; }
    .kpi-value  { font-size: 2rem; font-weight: 700; color: #E8EDF2; line-height: 1; }
    .kpi-delta  { font-size: 0.78rem; margin-top: 4px; }
    .kpi-good   { color: #3BCEAC; }
    .kpi-warn   { color: #E8A838; }
    .kpi-bad    { color: #D64045; }

    /* Alert box */
    .alert-box {
        background: #2B1B00;
        border-left: 4px solid #E8A838;
        border-radius: 6px;
        padding: 0.7rem 1rem;
        font-size: 0.85rem;
        margin-bottom: 0.5rem;
        color: #FFD580;
    }
    .alert-box.critical {
        background: #2B0000;
        border-left-color: #D64045;
        color: #FFB3B3;
    }

    /* Section headers */
    .section-header {
        font-size: 1.1rem;
        font-weight: 600;
        color: #2E86AB;
        border-bottom: 1px solid #1B3A5C;
        padding-bottom: 6px;
        margin: 1.2rem 0 0.8rem 0;
        letter-spacing: .04em;
    }

    /* Hide default header elements */
    #MainMenu, footer, header { visibility: hidden; }

    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        background: #122236;
        border-radius: 8px;
        gap: 4px;
        padding: 4px;
    }
    .stTabs [data-baseweb="tab"] {
        color: #8FA5BA !important;
        border-radius: 6px;
    }
    .stTabs [aria-selected="true"] {
        background: #1A2F47 !important;
        color: #3BCEAC !important;
    }

    /* DataFrame */
    .stDataFrame { border: 1px solid #1B3A5C; border-radius: 8px; }

    h1, h2, h3 { color: #E8EDF2 !important; }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# DATA
# ─────────────────────────────────────────────
RAW = """Date	Children apprehended and placed in CBP custody	Children in CBP custody	Children transferred out of CBP custody	Children in HHS Care	Children discharged from HHS Care
December 21, 2025	6	18	11	2484	14
December 18, 2025	11	50	6	2472	16
December 17, 2025	7	31	11	2481	10
December 16, 2025	8	54	15	2468	9
December 15, 2025	11	42	9	2470	7
December 14, 2025	8	35	4	2462	8
December 11, 2025	7	47	9	2437	10
December 10, 2025	10	54	5	2439	9
December 09, 2025	4	30	7	2443	8
December 08, 2025	9	27	9	2440	4
December 07, 2025	4	24	13	2429	12
December 04, 2025	16	39	7	2418	13
December 03, 2025	4	32	8	2419	7
December 02, 2025	7	34	6	2407	8
December 01, 2025	4	26	4	2410	9
November 30, 2025	4	18	10	2415	0
November 27, 2025	4	24	8	2389	7
November 25, 2025	6	47	14	2375	11
November 24, 2025	9	40	9	2371	13
November 23, 2025	3	46	22	2375	1
November 20, 2025	18	57	8	2340	9
November 19, 2025	7	32	3	2340	10
November 18, 2025	2	38	8	2345	12
November 17, 2025	1	35	6	2343	8
November 16, 2025	5	22	3	2340	5
November 13, 2025	6	26	16	2317	5
November 12, 2025	14	48	20	2302	7
November 11, 2025	11	39	12	2294	14
November 09, 2025	11	33	5	2294	4
November 06, 2025	6	33	9	2264	19
November 05, 2025	8	41	8	2272	7
November 04, 2025	6	33	6	2270	8
November 03, 2025	3	28	5	2269	12
November 02, 2025	5	21	10	2277	7
October 30, 2025	3	17	14	2287	12
October 29, 2025	6	25	4	2280	17
October 28, 2025	6	22	11	2286	6
October 27, 2025	2	31	8	2282	11
October 26, 2025	4	35	12	2276	10
October 23, 2025	4	27	26	2266	18
October 22, 2025	12	42	13	2261	12
October 21, 2025	13	39	17	2251	9
October 20, 2025	10	39	6	2243	7
October 19, 2025	9	34	17	2237	7
October 16, 2025	9	33	15	2233	9
October 15, 2025	8	29	10	2225	15
October 14, 2025	7	30	16	2235	8
October 13, 2025	8	24	7	2223	6
October 09, 2025	11	55	13	2192	12
October 08, 2025	8	49	15	2192	17
October 07, 2025	11	45	4	2189	10
October 06, 2025	5	33	15	2187	10
October 05, 2025	8	28	13	2180	16
October 02, 2025	20	51	15	2164	16
October 01, 2025	4	33	12	2163	14
September 30, 2025	8	32	12	2159	7
September 29, 2025	8	35	12	2148	13
September 28, 2025	11	29	12	2146	9
September 25, 2025	6	35	12	2132	18
September 24, 2025	3	38	12	2138	17
September 23, 2025	11	36	10	2145	15
September 22, 2025	17	40	14	2141	10
September 21, 2025	8	35	13	2134	5
September 18, 2025	20	52	11	2096	14
September 17, 2025	7	38	5	2096	13
September 16, 2025	7	28	17	2095	12
September 15, 2025	9	47	10	2086	10
September 14, 2025	7	39	13	2083	5
September 11, 2025	12	38	29	2047	6
September 10, 2025	10	47	14	2025	18
September 09, 2025	18	42	11	2023	14
September 08, 2025	7	25	5	2025	6
September 07, 2025	4	19	9	2026	7
September 04, 2025	11	40	2	2015	14
September 03, 2025	4	29	11	2019	10
September 02, 2025	6	35	9	2020	9
September 01, 2025	10	29	17	2010	5
August 28, 2025	8	33	6	1984	17
August 27, 2025	5	19	9	1988	19
August 26, 2025	10	21	20	1989	15
August 25, 2025	8	30	8	1980	11
August 24, 2025	4	21	5	1981	5
August 21, 2025	6	49	8	1972	21
August 20, 2025	10	38	10	1983	10
August 19, 2025	5	35	3	1980	11
August 18, 2025	4	20	6	1985	14
August 17, 2025	4	14	2	1991	3
August 14, 2025	3	27	4	1994	11
August 13, 2025	6	22	12	1997	17
August 12, 2025	8	38	9	1999	9
August 11, 2025	6	23	4	1999	16
August 10, 2025	0	18	8	2006	12
August 07, 2025	4	18	6	2031	17
August 06, 2025	4	17	3	2036	13
August 05, 2025	2	21	10	2042	14
August 04, 2025	5	22	11	2040	14
August 03, 2025	5	26	3	2049	5
July 31, 2025	2	9	6	2058	15
July 30, 2025	4	15	4	2063	16
July 29, 2025	2	8	3	2072	12
July 28, 2025	2	9	3	2080	14
July 27, 2025	1	12	2	2088	4
July 24, 2025	6	18	7	2096	29
July 23, 2025	6	21	5	2111	14
July 22, 2025	5	13	3	2117	16
July 21, 2025	4	18	7	2121	16
July 17, 2025	3	16	2	2153	17
July 16, 2025	1	9	0	2164	11
July 15, 2025	0	8	5	2171	17
July 14, 2025	2	9	1	2181	26
July 13, 2025	1	13	4	2204	10
July 10, 2025	2	12	3	2252	39
July 09, 2025	2	18	0	2281	32
July 08, 2025	5	16	8	2306	20
July 07, 2025	3	18	8	2317	20
July 06, 2025	4	17	2	2332	8
July 02, 2025	8	20	9	2373	38
July 01, 2025	7	14	6	2391	22
June 30, 2025	9	22	8	2407	16
June 29, 2025	5	17	7	2413	20
June 26, 2025	3	9	7	2447	35
June 25, 2025	6	12	2	2470	24
June 24, 2025	5	20	5	2489	16
June 23, 2025	3	15	5	2495	17
June 22, 2025	7	13	5	2508	7
June 19, 2025	8	19	7	2501	18
June 17, 2025	7	24	10	2523	14
June 10, 2025	17	28	7	2511	12
June 09, 2025	8	21	14	2516	9
June 08, 2025	10	16	15	2507	13
June 05, 2025	8	26	5	2503	21
June 04, 2025	4	16	9	2516	16
June 03, 2025	5	23	11	2519	15
June 02, 2025	10	19	5	2518	16
June 01, 2025	8	24	16	2528	12
May 29, 2025	13	38	15	2506	11
May 28, 2025	12	39	12	2499	14
May 27, 2025	6	24	7	2504	11
May 22, 2025	18	36	17	2473	15
May 21, 2025	14	62	13	2467	18
May 19, 2025	7	27	17	2457	6
May 18, 2025	13	28	14	2437	9
May 15, 2025	15	31	14	2410	14
May 14, 2025	7	30	14	2394	11
May 13, 2025	18	29	12	2394	11
May 12, 2025	7	33	14	2392	7
May 11, 2025	15	20	12	2385	3
May 08, 2025	15	24	16	2361	11
May 07, 2025	10	30	15	2335	10
May 06, 2025	10	33	16	2339	16
May 05, 2025	15	44	20	2331	17
May 04, 2025	9	31	10	2335	5
May 01, 2025	13	32	14	2306	16
April 30, 2025	7	34	9	2309	12
April 29, 2025	11	25	11	2304	15
April 28, 2025	6	26	12	2307	8
April 27, 2025	9	40	12	2301	4
April 24, 2025	3	9	7	2294	13
April 23, 2025	3	23	4	2300	11
April 22, 2025	7	19	14	2305	17
April 21, 2025	10	25	5	2308	6
April 20, 2025	4	15	6	2305	4
April 17, 2025	7	26	10	2288	14
April 16, 2025	11	30	5	2291	8
April 15, 2025	4	19	12	2286	7
April 14, 2025	5	26	9	2282	13
April 13, 2025	5	26	10	2283	3
April 11, 2025	8	22	8	2267	9
April 10, 2025	18	25	17	2265	6
April 09, 2025	6	19	10	2251	5
April 08, 2025	12	34	12	2243	9
April 07, 2025	12	22	9	2237	5
April 06, 2025	7	14	7	2234	11
April 03, 2025	12	26	18	2223	8
April 02, 2025	5	31	16	2208	3
April 01, 2025	17	36	7	2191	12
March 31, 2025	9	25	8	2193	5
March 30, 2025	9	20	5	2188	2
March 27, 2025	1	19	13	2159	2
March 26, 2025	9	21	15	2159	2
March 25, 2025	12	19	7	2145	6
March 24, 2025	7	13	11	2139	7
March 23, 2025	15	29	9	2136	2
March 20, 2025	9	20	11	2124	7
March 19, 2025	6	22	14	2119	9
March 18, 2025	19	34	6	2109	8
March 17, 2025	5	14	0	2111	8
March 16, 2025	1	9	8	2117	5
March 13, 2025	4	20	9	2116	6
March 12, 2025	6	18	2	2113	8
March 11, 2025	3	11	7	2116	20
March 10, 2025	6	28	8	2125	23
March 09, 2025	12	25	15	2137	30
March 06, 2025	7	27	6	2218	33
March 05, 2025	5	20	4	2238	40
March 04, 2025	4	25	10	2272	30
March 03, 2025	8	29	18	2287	25
March 02, 2025	12	24	4	2297	31
February 27, 2025	10	15	17	2391	37
February 26, 2025	12	21	1	2411	23
February 25, 2025	11	7	7	2413	23
February 24, 2025	20	22	14	2413	24
February 23, 2025	7	16	8	2423	35
February 20, 2025	13	25	15	2520	32
February 19, 2025	12	17	17	2528	19
February 18, 2025	18	19	11	2536	9
February 17, 2025	8	17	14	2532	15
February 13, 2025	15	10	23	2703	72
February 12, 2025	16	20	20	2752	66
February 11, 2025	11	22	12	2799	50
February 10, 2025	16	18	15	2834	63
February 09, 2025	15	13	23	2878	99
February 06, 2025	25	32	27	3181	145
February 05, 2025	26	36	36	3290	104
February 04, 2025	34	54	29	3359	74
February 03, 2025	23	45	11	3403	102
February 02, 2025	20	22	41	3483	168
January 30, 2025	47	42	47	3923	159
January 29, 2025	32	50	39	4036	99
January 28, 2025	32	49	39	4096	101
January 27, 2025	33	53	34	4161	127
January 26, 2025	29	51	11	4241	182
January 23, 2025	91	75	97	4621	174
January 22, 2025	62	97	52	4717	83
January 21, 2025	59	64	117	4728	54
January 20, 2025	84	118	136	4638	127
January 19, 2025	86	152	168	4628	176
January 16, 2025	106	196	131	4881	159
January 15, 2025	113	162	107	4903	164
January 14, 2025	92	124	93	4957	139
January 13, 2025	68	107	102	5019	181
January 12, 2025	74	103	80	5092	235
January 09, 2025	56	82	68	5507	164
January 08, 2025	38	80	82	5605	184
January 07, 2025	65	83	65	5703	133
January 06, 2025	41	60	71	5769	190
January 05, 2025	43	73	64	5882	185
January 02, 2025	35	70	53	6292	170
January 01, 2025	25	66	94	6405	144
December 30, 2024	99	156	139	6454	177
December 29, 2024	107	170	133	6465	216
December 26, 2024	80	122	152	6707	135
December 25, 2024	57	162	193	6689	107
December 24, 2024	161	304	211	6622	155
December 23, 2024	205	294	177	6548	231
December 22, 2024	100	255	236	6595	268
December 19, 2024	269	412	204	6600	238
December 18, 2024	168	285	210	6598	134
December 17, 2024	187	310	247	6506	151
December 16, 2024	133	287	189	6454	149
December 15, 2024	180	337	219	6408	224
December 12, 2024	153	253	286	6481	194
December 11, 2024	209	353	232	6402	152
December 10, 2024	167	326	213	6310	149
December 09, 2024	224	315	152	6268	174
December 08, 2024	132	243	183	6286	172
December 05, 2024	218	283	208	6310	150
December 04, 2024	118	245	160	6269	115
December 03, 2024	81	230	242	6192	107
December 02, 2024	236	330	222	6061	115
December 01, 2024	196	306	187	5986	149
November 28, 2024	113	280	237	5963	143
November 27, 2024	239	367	224	5862	211
November 26, 2024	152	272	214	5826	112
November 25, 2024	170	297	196	5715	129
November 24, 2024	191	283	192	5664	207
November 21, 2024	109	214	173	5850	210
November 20, 2024	155	212	181	5879	148
November 19, 2024	119	209	152	5844	146
November 18, 2024	143	203	163	5819	138
November 17, 2024	105	210	149	5816	195
November 14, 2024	119	219	210	6025	172
November 13, 2024	148	245	175	5966	151
November 12, 2024	142	235	139	5975	138
November 11, 2024	118	139	168	5963	145
November 07, 2024	125	232	192	6084	177
November 06, 2024	156	256	176	6086	137
November 05, 2024	109	245	159	6045	126
November 04, 2024	167	209	157	6007	132
November 03, 2024	84	171	157	5990	184
October 31, 2024	87	246	173	6148	177
October 30, 2024	136	276	178	6149	160
October 29, 2024	166	277	229	6106	126
October 28, 2024	110	272	193	6008	156
October 27, 2024	202	313	158	5974	192
October 23, 2024	134	294	186	6077	138
October 22, 2024	180	280	146	6043	109
October 21, 2024	108	220	213	5966	154
October 20, 2024	147	276	214	5918	195
October 17, 2024	104	230	206	6076	160
October 16, 2024	174	285	150	6036	129
October 15, 2024	113	208	159	6013	107
October 14, 2024	88	214	160	5935	106
October 13, 2024	130	227	192	5889	210
October 10, 2024	84	158	193	6075	159
October 09, 2024	115	216	169	6047	137
October 08, 2024	167	239	166	6013	123
October 07, 2024	99	190	176	5968	153
October 03, 2024	101	162	178	6118	193
October 02, 2024	107	215	230	6091	173
October 01, 2024	184	314	217	6040	137
September 30, 2024	209	285	184	5967	138
September 29, 2024	81	213	153	5925	177
September 26, 2024	91	199	172	6090	185
September 25, 2024	154	225	220	6050	169
September 24, 2024	186	259	172	6023	143
September 23, 2024	92	203	173	6002	165
September 22, 2024	124	234	161	5989	197
September 19, 2024	93	196	169	6270	188
September 18, 2024	116	213	217	6245	149
September 17, 2024	159	304	139	6227	160
September 16, 2024	113	209	160	6229	164
September 15, 2024	98	220	167	6234	210
September 13, 2024	81	200	212	6326	279
September 12, 2024	184	280	210	6360	220
September 11, 2024	93	248	175	6410	162
September 10, 2024	131	251	180	6396	148
September 09, 2024	144	275	190	6353	141
September 08, 2024	123	255	164	6312	221
September 05, 2024	126	230	175	6448	121
September 04, 2024	121	231	219	6375	114
September 03, 2024	131	263	177	6272	112
September 02, 2024	133	270	198	6192	129
August 29, 2024	145	295	188	6250	169
August 28, 2024	170	285	178	6227	134
August 27, 2024	149	285	222	6152	97
August 22, 2024	182	307	205	6054	171
August 21, 2024	134	245	167	6028	156
August 20, 2024	136	274	245	5995	112
August 19, 2024	176	254	162	5865	158
August 18, 2024	86	244	235	5821	178
August 15, 2024	124	241	156	5895	220
August 14, 2024	109	226	191	5987	178
August 13, 2024	162	239	189	5981	123
August 12, 2024	109	219	155	5903	148
August 11, 2024	95	211	140	5894	249
August 08, 2024	119	230	213	6084	174
August 07, 2024	135	273	207	6038	174
August 06, 2024	163	283	200	5998	143
August 05, 2024	172	259	138	5950	150
August 04, 2024	63	167	143	5943	170
August 01, 2024	227	298	212	6016	169
July 31, 2024	140	261	163	5963	154
July 30, 2024	125	203	208	5930	92
July 29, 2024	114	210	219	5819	163
July 28, 2024	152	290	199	5743	207
July 25, 2024	93	198	208	5954	194
July 24, 2024	137	272	166	5927	177
July 23, 2024	120	257	126	5965	170
July 22, 2024	102	189	155	6002	234
July 21, 2024	90	196	205	6058	262
July 17, 2024	128	228	177	6228	187
July 16, 2024	136	246	123	6239	173
July 15, 2024	105	185	158	6283	171
July 14, 2024	116	188	164	6308	237
July 11, 2024	80	176	125	6640	197
July 10, 2024	150	157	201	6649	177
July 09, 2024	116	181	182	6651	130
July 08, 2024	141	173	129	6617	123
July 07, 2024	96	160	233	6599	213
July 04, 2024	158	226	191	6790	225
July 02, 2024	141	232	188	6823	184
July 01, 2024	123	233	159	6825	229
June 30, 2024	123	230	167	6874	273
June 27, 2024	174	208	256	7248	268
June 26, 2024	132	235	197	7268	187
June 25, 2024	172	263	191	7239	202
June 24, 2024	116	175	172	7239	202
June 23, 2024	102	227	201	7247	294
June 20, 2024	145	247	243	7431	235
June 19, 2024	204	321	246	7433	198
June 18, 2024	160	297	253	7340	214
June 17, 2024	159	310	272	7318	224
June 16, 2024	204	315	233	7307	294
June 13, 2024	167	293	230	7544	259
June 12, 2024	152	266	274	7548	212
June 11, 2024	186	352	224	7493	156
June 10, 2024	184	334	229	7439	212
June 09, 2024	116	289	166	7451	312
June 06, 2024	179	326	282	7741	238
June 05, 2024	173	345	291	7691	198
June 04, 2024	260	356	176	7565	203
June 03, 2024	109	244	257	7596	224
June 02, 2024	159	330	322	7546	306
May 30, 2024	167	406	339	7563	190
May 29, 2024	182	462	158	7491	141
May 28, 2024	153	348	239	7418	151
May 27, 2024	156	344	252	7365	167
May 23, 2024	193	272	314	7494	227
May 22, 2024	168	349	272	7474	208
May 21, 2024	196	348	176	7404	145
May 20, 2024	111	268	217	7368	192
May 19, 2024	143	295	278	7356	298
May 16, 2024	206	340	214	7565	234
May 15, 2024	115	285	341	7589	265
May 14, 2024	246	419	218	7546	186
May 13, 2024	112	331	167	7499	157
May 12, 2024	138	301	263	7464	245
May 09, 2024	138	285	268	7570	244
May 08, 2024	167	374	205	7583	202
May 07, 2024	176	334	246	7566	163
May 06, 2024	173	337	211	7449	205
May 05, 2024	150	315	228	7447	332
May 02, 2024	206	411	293	7577	194
May 01, 2024	197	437	295	7508	190
April 30, 2024	220	443	194	7431	135
April 29, 2024	140	292	255	7373	187
April 28, 2024	158	349	365	7298	250
April 25, 2024	145	357	333	7209	217
April 24, 2024	253	411	307	7128	154
April 23, 2024	252	427	307	6967	134
April 22, 2024	176	424	251	6799	214
April 21, 2024	208	380	343	6745	240
April 18, 2024	144	322	258	6728	260
April 17, 2024	182	371	274	6725	227
April 16, 2024	219	392	205	6685	163
April 15, 2024	144	303	176	6681	191
April 14, 2024	128	245	243	6630	290
April 11, 2024	183	221	220	6912	285
April 10, 2024	117	244	142	6999	227
April 09, 2024	118	231	217	7043	130
April 08, 2024	102	230	167	6988	199
April 07, 2024	106	239	233	6982	279
April 04, 2024	95	226	152	7317	225
April 03, 2024	124	230	190	7346	163
April 02, 2024	101	230	175	7340	132
April 01, 2024	109	235	171	7271	172
March 31, 2024	105	254	151	7257	287
March 28, 2024	161	288	248	7762	360
March 27, 2024	129	287	185	7893	215
March 26, 2024	187	276	200	7919	208
March 25, 2024	128	242	224	7899	229
March 24, 2024	124	264	221	7899	373
March 21, 2024	132	261	141	8292	235
March 20, 2024	91	181	174	8365	227
March 19, 2024	99	202	256	8390	197
March 18, 2024	123	243	188	8333	283
March 17, 2024	127	260	259	8373	342
March 14, 2024	166	301	252	8695	310
March 13, 2024	165	358	167	8819	239
March 12, 2024	154	294	290	8843	213
March 11, 2024	178	336	290	8757	253
March 10, 2024	190	368	326	8714	373
March 07, 2024	181	424	328	8902	305
March 06, 2024	230	457	277	8870	232
March 05, 2024	246	472	345	8800	214
March 04, 2024	225	509	340	8660	229
March 03, 2024	236	468	347	8594	354
February 29, 2024	262	444	354	8724	299
February 28, 2024	209	447	274	8699	257
February 27, 2024	197	369	306	8650	206
February 26, 2024	199	438	326	8404	329
February 25, 2024	244	482	366	8404	329
February 22, 2024	165	400	292	8607	293
February 21, 2024	232	430	318	8573	231
February 20, 2024	149	395	273	8488	192
February 19, 2024	249	420	371	8380	218
February 15, 2024	333	508	272	8463	312
February 14, 2024	185	322	272	8512	230
February 13, 2024	227	369	349	8348	160
February 12, 2024	213	430	440	8092	234
February 11, 2024	205	515	226	8056	347
February 08, 2024	298	499	358	8188	315
February 07, 2024	227	453	330	8160	222
February 06, 2024	291	455	323	8045	178
February 05, 2024	157	466	345	7872	242
February 04, 2024	253	531	248	7813	342
February 01, 2024	222	459	289	8026	337
January 31, 2024	203	477	258	8153	266
January 30, 2024	93	198	208	8182	187
January 29, 2024	137	272	166	8057	195
January 28, 2024	120	257	126	8004	307
January 25, 2024	102	189	155	8180	293
January 24, 2024	90	196	205	8212	243
January 23, 2024	128	228	177	8133	202
January 22, 2024	136	246	123	8008	222
January 21, 2024	105	185	158	7974	371
January 18, 2024	116	188	164	8042	359
January 17, 2024	80	176	125	8072	353
January 16, 2024	32	49	39	8133	188
January 15, 2024	33	53	34	8033	234
January 11, 2024	29	51	11	8829	476
January 10, 2024	91	75	97	9144	349
January 09, 2024	62	97	52	9311	286
January 08, 2024	59	64	117	9670	367
January 07, 2024	84	118	136	9670	367
January 04, 2024	86	152	168	10558	362
January 03, 2024	106	196	131	10718	263
January 02, 2024	113	162	107	10770	316
January 01, 2024	92	124	93	10870	290
December 28, 2023	68	107	102	11230	357
December 27, 2023	74	103	80	11206	335
December 26, 2023	56	82	68	11217	288
December 25, 2023	90	196	205	11144	347
December 21, 2023	128	228	177	11375	497
December 20, 2023	136	246	123	11516	390
December 19, 2023	105	185	158	11291	272
December 18, 2023	116	188	164	11149	364
December 17, 2023	80	176	125	11092	456
December 14, 2023	150	157	201	11242	396
December 13, 2023	116	181	182	11192	335
December 12, 2023	141	173	129	11077	259
December 11, 2023	96	160	233	10998	304
December 10, 2023	158	226	191	10871	411
December 07, 2023	141	232	188	10897	466
December 06, 2023	123	233	159	10832	376
December 05, 2023	123	230	167	10761	261
December 04, 2023	174	208	256	10635	273
December 03, 2023	132	235	197	10579	417
November 30, 2023	92	124	93	10536	320
November 29, 2023	68	107	102	10398	284
November 28, 2023	74	103	80	10223	223
November 27, 2023	56	82	68	10123	214
November 26, 2023	90	196	205	9845	312
November 23, 2023	128	228	177	9838	283
November 21, 2023	136	246	123	9804	250
November 20, 2023	105	185	158	9638	298
November 19, 2023	116	188	164	9573	435
November 16, 2023	80	176	125	9762	374
November 15, 2023	150	157	201	9762	316
November 14, 2023	116	181	182	9665	247
November 13, 2023	141	173	129	9510	287
November 12, 2023	96	160	233	9477	313
November 08, 2023	158	226	191	9634	310
November 07, 2023	141	232	188	9483	231
November 06, 2023	123	233	159	9286	316
November 05, 2023	123	230	167	9273	370
November 02, 2023	174	208	256	9442	330
November 01, 2023	132	235	197	9250	279
October 31, 2023	33	53	34	9072	295
October 30, 2023	29	51	11	9026	278
October 29, 2023	91	75	97	8925	418
October 26, 2023	62	97	52	9235	390
October 25, 2023	59	64	117	9351	293
October 24, 2023	84	118	136	9396	300
October 23, 2023	86	152	168	9436	327
October 22, 2023	106	196	131	9506	454
October 19, 2023	113	162	107	10319	406
October 18, 2023	92	124	93	10511	393
October 17, 2023	68	107	102	10630	315
October 16, 2023	74	103	80	10629	331
October 15, 2023	56	82	68	10571	434
October 12, 2023	38	80	82	10992	398
October 11, 2023	65	83	65	10960	266
October 10, 2023	41	60	71	10910	257
October 09, 2023	43	73	64	10815	282
October 05, 2023	35	70	53	11130	427
October 04, 2023	25	66	94	10963	330
October 03, 2023	99	156	139	10818	287
October 02, 2023	107	170	133	10724	284
October 01, 2023	80	122	152	10598	493
September 28, 2023	57	162	193	10984	447
September 27, 2023	161	304	211	11017	331
September 26, 2023	205	294	177	10978	332
September 25, 2023	100	255	236	10842	284
September 24, 2023	269	412	204	10744	403
September 21, 2023	168	285	210	11067	428
September 20, 2023	187	310	247	11064	364
September 19, 2023	133	287	189	11095	260
September 18, 2023	180	337	219	10892	313
September 17, 2023	153	253	286	10799	427
September 14, 2023	209	353	232	10837	414
September 13, 2023	167	326	213	10678	343
September 12, 2023	224	315	152	10649	316
September 11, 2023	132	243	183	10492	277
September 10, 2023	218	283	208	10282	382
September 07, 2023	118	245	160	10419	398
September 06, 2023	81	230	242	10356	291
September 05, 2023	236	330	222	10142	243
September 04, 2023	196	306	187	9988	293
August 31, 2023	113	280	237	10140	505
August 30, 2023	239	367	224	10280	366
August 29, 2023	152	272	214	10180	286
August 28, 2023	170	297	196	10012	388
August 27, 2023	191	283	192	9873	488
August 24, 2023	109	214	173	10026	443
August 23, 2023	155	212	181	10071	285
August 22, 2023	119	209	152	9921	230
August 21, 2023	143	203	163	9668	281
August 20, 2023	105	210	149	9483	390
August 17, 2023	119	219	210	9694	407
August 16, 2023	148	245	175	9634	288
August 10, 2023	142	235	139	8914	353
August 09, 2023	118	139	168	8888	251
August 08, 2023	125	232	192	8725	207
August 07, 2023	156	256	176	8493	202
August 06, 2023	109	245	159	8298	322
August 03, 2023	167	209	157	8294	339
August 02, 2023	84	171	157	8261	271
August 01, 2023	87	246	173	8103	168
July 31, 2023	136	276	178	7800	220
July 30, 2023	166	277	229	7671	305
July 27, 2023	110	272	193	7754	259
July 26, 2023	202	313	158	7647	215
July 25, 2023	134	294	186	7510	136
July 24, 2023	180	280	146	7220	187
July 23, 2023	108	220	213	7052	276
July 20, 2023	147	276	214	7116	281
July 19, 2023	104	230	206	7001	226
July 18, 2023	174	285	150	6874	181
July 17, 2023	113	208	159	6632	160
July 16, 2023	88	214	160	6468	218
July 13, 2023	130	227	192	6604	226
July 12, 2023	84	158	193	6521	210
July 11, 2023	115	216	169	6498	143
July 10, 2023	167	239	166	6346	163
July 09, 2023	99	190	176	6214	196
July 06, 2023	101	162	178	6239	205
July 05, 2023	107	215	230	6193	167
July 04, 2023	184	314	217	6127	124
July 02, 2023	209	285	184	5903	309
June 29, 2023	81	213	153	6058	213
June 28, 2023	91	199	172	5999	174
June 27, 2023	154	225	220	5917	155
June 26, 2023	186	259	172	5819	174
June 25, 2023	92	203	173	5766	263
June 22, 2023	124	234	161	5956	207
June 21, 2023	93	196	169	5922	149
June 20, 2023	33	53	34	5904	134
June 19, 2023	29	51	11	5679	142
June 15, 2023	91	75	97	6038	272
June 14, 2023	62	97	52	6065	167
June 13, 2023	59	64	117	6061	146
June 12, 2023	84	118	136	6021	177
June 11, 2023	86	152	168	6007	238
June 08, 2023	106	196	131	6446	255
June 07, 2023	113	162	107	6483	208
June 06, 2023	92	124	93	6508	187
June 05, 2023	68	107	102	6523	189
June 04, 2023	74	103	80	6555	292
June 01, 2023	56	82	68	7002	287
May 31, 2023	38	80	82	7053	210
May 30, 2023	65	83	65	7046	168
May 29, 2023	41	60	71	6996	207
May 25, 2023	43	73	64	7546	408
May 24, 2023	35	70	53	7709	276
May 23, 2023	25	66	94	7788	246
May 22, 2023	99	156	139	7848	240
May 21, 2023	107	170	133	7826	343
May 18, 2023	80	122	152	8474	351
May 17, 2023	57	162	193	8569	307
May 16, 2023	161	304	211	8572	272
May 15, 2023	205	294	177	8571	277
May 14, 2023	100	255	236	8445	288
May 11, 2023	269	412	204	8672	392
May 10, 2023	168	285	210	8681	304
May 09, 2023	187	310	247	8606	250
May 08, 2023	133	287	189	8590	261
May 07, 2023	180	337	219	8485	375
May 04, 2023	153	253	286	8790	332
May 03, 2023	209	353	232	8704	267
May 02, 2023	167	326	213	8654	245
May 01, 2023	224	315	152	8492	237
April 30, 2023	132	243	183	8352	293
April 27, 2023	218	283	208	8159	310
April 26, 2023	118	245	160	8117	256
April 25, 2023	81	230	242	8017	202
April 24, 2023	236	330	222	7796	213
April 23, 2023	196	306	187	7534	266
April 20, 2023	113	280	237	7490	320
April 19, 2023	239	367	224	7356	229
April 18, 2023	152	272	214	7376	234
April 17, 2023	170	297	196	7344	248
April 16, 2023	191	283	192	7380	272
April 13, 2023	109	214	173	7795	370
April 12, 2023	155	212	181	7876	283
April 11, 2023	119	209	152	7922	187
April 10, 2023	143	203	163	7826	265
April 09, 2023	105	210	149	7900	329
April 06, 2023	119	219	210	8178	284
April 05, 2023	148	245	175	8175	260
April 04, 2023	142	235	139	8068	259
April 03, 2023	118	139	168	8054	284
April 02, 2023	125	232	192	7981	304
March 30, 2023	156	256	176	8158	359
March 29, 2023	109	245	159	8208	267
March 28, 2023	167	209	157	8079	223
March 27, 2023	84	171	157	7994	235
March 26, 2023	87	246	173	7847	352
March 23, 2023	136	276	178	8102	331
March 22, 2023	166	277	229	8097	246
March 21, 2023	110	272	193	8050	221
March 20, 2023	202	313	158	7931	279
March 19, 2023	134	294	186	7885	306
March 16, 2023	180	280	146	7989	308
March 15, 2023	108	220	213	7915	286
March 14, 2023	147	276	214	7810	181
March 13, 2023	104	230	206	7567	249
March 09, 2023	174	285	150	7786	340
March 08, 2023	113	208	159	7885	291
March 07, 2023	88	214	160	7859	259
March 02, 2023	130	227	192	7870	335
March 01, 2023	84	158	193	7930	307
February 28, 2023	115	216	169	7896	200
February 27, 2023	167	239	166	7800	248
February 26, 2023	99	190	176	7609	323
February 23, 2023	101	162	178	7914	386
February 22, 2023	107	215	230	7978	232
February 21, 2023	184	314	217	7967	213
February 20, 2023	209	285	184	7817	209
February 16, 2023	81	213	153	7793	361
February 15, 2023	91	199	172	7869	290
February 14, 2023	154	225	220	7794	223
February 13, 2023	186	259	172	7483	244
February 12, 2023	92	203	173	7434	317
February 09, 2023	124	234	161	7908	353
February 08, 2023	93	196	169	7915	317
February 07, 2023	16	20	20	7855	200
February 06, 2023	11	22	12	7720	196
February 05, 2023	16	18	15	7586	342
February 02, 2023	15	13	23	7879	298
February 01, 2023	25	32	27	7903	231
January 31, 2023	26	36	36	7803	158
January 30, 2023	34	54	29	7743	196
January 29, 2023	23	45	11	7472	303
January 25, 2023	20	22	41	7538	180
January 24, 2023	47	42	47	7433	175
January 23, 2023	32	50	39	7280	181
January 22, 2023	32	49	39	7122	227
January 12, 2023	33	53	34	6566	436"""

@st.cache_data
def load_data():
    df = pd.read_csv(StringIO(RAW), sep="\t")
    df.columns = ["Date", "CBP_Apprehended", "CBP_Custody", "CBP_Transferred", "HHS_Care", "HHS_Discharged"]
    df["Date"] = pd.to_datetime(df["Date"])
    df = df.sort_values("Date").reset_index(drop=True)
    df["Month"]   = df["Date"].dt.to_period("M").dt.to_timestamp()
    df["YearMonth"] = df["Date"].dt.strftime("%b %Y")
    df["DayOfWeek"] = df["Date"].dt.day_name()
    df["IsWeekend"] = df["Date"].dt.dayofweek >= 5

    # KPI metrics
    df["Transfer_Efficiency"]   = df["CBP_Transferred"] / df["CBP_Custody"].replace(0, np.nan)
    df["Discharge_Effectiveness"] = df["HHS_Discharged"] / df["HHS_Care"].replace(0, np.nan)
    df["Pipeline_Throughput"]   = (df["CBP_Transferred"] + df["HHS_Discharged"]) / (df["CBP_Apprehended"] + df["CBP_Transferred"]).replace(0, np.nan)
    df["Backlog_Delta"]         = df["CBP_Apprehended"] - df["CBP_Transferred"]
    df["Outcome_Stability"]     = df["HHS_Discharged"].rolling(7, min_periods=1).std()

    return df

df = load_data()

# ─────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🏛️ UAC Analytics")
    st.markdown("**Care Transition Efficiency**")
    st.markdown("---")

    min_date, max_date = df["Date"].min().date(), df["Date"].max().date()
    date_range = st.date_input(
        "📅 Date Range",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date
    )

    st.markdown("---")
    st.markdown("**⚠️ Alert Thresholds**")
    te_thresh = st.slider("Transfer Efficiency Alert", 0.0, 1.0, 0.20, 0.05,
                          help="Flag days where transfers < this × CBP custody")
    de_thresh = st.slider("Discharge Effectiveness Alert", 0.0, 0.1, 0.02, 0.005,
                          format="%.3f",
                          help="Flag days where discharges < this × HHS census")

    st.markdown("---")
    st.markdown("**📊 Metric Toggles**")
    show_ter  = st.checkbox("Transfer Efficiency Ratio", True)
    show_dei  = st.checkbox("Discharge Effectiveness Index", True)
    show_pt   = st.checkbox("Pipeline Throughput", True)
    show_back = st.checkbox("Backlog Accumulation", True)

    st.markdown("---")
    st.caption("ShadowFox AIML Internship · UAC Program")

# ─────────────────────────────────────────────
# FILTER
# ─────────────────────────────────────────────
if isinstance(date_range, tuple) and len(date_range) == 2:
    start_d, end_d = date_range
    fdf = df[(df["Date"].dt.date >= start_d) & (df["Date"].dt.date <= end_d)].copy()
else:
    fdf = df.copy()

# ─────────────────────────────────────────────
# HEADER
# ─────────────────────────────────────────────
st.markdown("""
<div style="padding: 1rem 0 0.5rem 0; border-bottom: 2px solid #1B3A5C; margin-bottom: 1.2rem;">
  <div style="font-size:0.78rem; color:#8FA5BA; letter-spacing:.1em; text-transform:uppercase; margin-bottom:4px;">
    U.S. Department of Health and Human Services · UAC Program
  </div>
  <div style="font-size:1.8rem; font-weight:700; color:#E8EDF2; line-height:1.1;">
    Care Transition Efficiency & Placement Outcome Analytics
  </div>
  <div style="font-size:0.85rem; color:#8FA5BA; margin-top:6px;">
    {rows} reporting days · {start} → {end}
  </div>
</div>
""".format(
    rows=len(fdf),
    start=fdf["Date"].min().strftime("%b %d, %Y") if len(fdf) else "—",
    end=fdf["Date"].max().strftime("%b %d, %Y") if len(fdf) else "—"
), unsafe_allow_html=True)

# ─────────────────────────────────────────────
# ALERTS
# ─────────────────────────────────────────────
low_te  = fdf[fdf["Transfer_Efficiency"] < te_thresh]
low_de  = fdf[fdf["Discharge_Effectiveness"] < de_thresh]
high_bl = fdf[fdf["Backlog_Delta"] > fdf["Backlog_Delta"].quantile(0.90)]

if len(low_te) or len(low_de) or len(high_bl):
    st.markdown('<div class="section-header">⚠️ Active Alerts</div>', unsafe_allow_html=True)
    acol1, acol2, acol3 = st.columns(3)
    with acol1:
        if len(low_te):
            st.markdown(f'<div class="alert-box">Low Transfer Efficiency on <b>{len(low_te)}</b> days (below {te_thresh:.0%} threshold)</div>', unsafe_allow_html=True)
    with acol2:
        if len(low_de):
            st.markdown(f'<div class="alert-box critical">Low Discharge Effectiveness on <b>{len(low_de)}</b> days (below {de_thresh:.3f} threshold)</div>', unsafe_allow_html=True)
    with acol3:
        if len(high_bl):
            st.markdown(f'<div class="alert-box">High Backlog Accumulation on <b>{len(high_bl)}</b> days (top 10% severity)</div>', unsafe_allow_html=True)

# ─────────────────────────────────────────────
# KPI CARDS
# ─────────────────────────────────────────────
st.markdown('<div class="section-header">📌 Key Performance Indicators</div>', unsafe_allow_html=True)

k1, k2, k3, k4, k5 = st.columns(5)

avg_te  = fdf["Transfer_Efficiency"].mean()
avg_dei = fdf["Discharge_Effectiveness"].mean()
avg_pt  = fdf["Pipeline_Throughput"].mean()
avg_bl  = fdf["Backlog_Delta"].mean()
avg_os  = fdf["Outcome_Stability"].mean()

latest_hhs = fdf["HHS_Care"].iloc[-1] if len(fdf) else 0

def kpi_html(label, value, delta_txt, cls):
    return f"""
    <div class="kpi-card">
        <div class="kpi-label">{label}</div>
        <div class="kpi-value">{value}</div>
        <div class="kpi-delta {cls}">{delta_txt}</div>
    </div>"""

with k1:
    cls = "kpi-good" if avg_te > 0.40 else ("kpi-warn" if avg_te > 0.20 else "kpi-bad")
    st.markdown(kpi_html("Transfer Efficiency", f"{avg_te:.1%}", "CBP→HHS speed", cls), unsafe_allow_html=True)

with k2:
    cls = "kpi-good" if avg_dei > 0.04 else ("kpi-warn" if avg_dei > 0.02 else "kpi-bad")
    st.markdown(kpi_html("Discharge Effectiveness", f"{avg_dei:.2%}", "Placement rate", cls), unsafe_allow_html=True)

with k3:
    cls = "kpi-good" if avg_pt > 1.5 else ("kpi-warn" if avg_pt > 1.0 else "kpi-bad")
    st.markdown(kpi_html("Pipeline Throughput", f"{avg_pt:.2f}x", "Exits / entries", cls), unsafe_allow_html=True)

with k4:
    cls = "kpi-bad" if avg_bl > 20 else ("kpi-warn" if avg_bl > 5 else "kpi-good")
    st.markdown(kpi_html("Avg Backlog/Day", f"{avg_bl:+.1f}", "Apprehended − Transferred", cls), unsafe_allow_html=True)

with k5:
    st.markdown(kpi_html("Current HHS Census", f"{latest_hhs:,}", "Children in care (latest)", "kpi-warn"), unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# TABS
# ─────────────────────────────────────────────
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "🔄 Pipeline Flow",
    "📈 Efficiency Metrics",
    "🚨 Bottleneck Detection",
    "📊 Outcome Trends",
    "🗓️ Temporal Patterns"
])

COLORS = {
    "cbp_apprehended": "#2E86AB",
    "cbp_custody":     "#3BCEAC",
    "cbp_transfer":    "#E8A838",
    "hhs_care":        "#D64045",
    "hhs_discharged":  "#9B5DE5",
    "te":              "#3BCEAC",
    "dei":             "#E8A838",
    "pt":              "#9B5DE5",
    "backlog":         "#D64045",
}
LAYOUT = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(color="#E8EDF2", family="Inter, sans-serif"),
    xaxis=dict(gridcolor="#1B3A5C", linecolor="#1B3A5C"),
    yaxis=dict(gridcolor="#1B3A5C", linecolor="#1B3A5C"),
    margin=dict(l=50, r=30, t=40, b=40),
    hovermode="x unified",
    legend=dict(bgcolor="rgba(0,0,0,0)", bordercolor="#1B3A5C", borderwidth=1)
)

# ── Tab 1: Pipeline Flow ──────────────────────
with tab1:
    st.markdown('<div class="section-header">Care Pipeline Flow — Population Over Time</div>', unsafe_allow_html=True)

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=fdf["Date"], y=fdf["HHS_Care"],
                             name="Children in HHS Care", fill="tozeroy",
                             fillcolor="rgba(214,64,69,0.12)", line=dict(color=COLORS["hhs_care"], width=2)))
    fig.add_trace(go.Scatter(x=fdf["Date"], y=fdf["CBP_Custody"],
                             name="Children in CBP Custody", fill="tozeroy",
                             fillcolor="rgba(59,206,172,0.12)", line=dict(color=COLORS["cbp_custody"], width=1.5)))
    fig.add_trace(go.Bar(x=fdf["Date"], y=fdf["HHS_Discharged"],
                         name="Daily HHS Discharges", marker_color=COLORS["hhs_discharged"],
                         opacity=0.6, yaxis="y2"))
    fig.update_layout(
        title="Pipeline Census & Daily Placements",
        yaxis=dict(title="Children in Care", gridcolor="#1B3A5C", linecolor="#1B3A5C"),
        yaxis2=dict(title="Daily Discharges", overlaying="y", side="right",
                    gridcolor="rgba(0,0,0,0)", linecolor="#1B3A5C"),
        height=420
    )
    st.plotly_chart(fig, use_container_width=True)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<div class="section-header">Daily Transfer Volume</div>', unsafe_allow_html=True)
        fig2 = go.Figure()
        fig2.add_trace(go.Bar(x=fdf["Date"], y=fdf["CBP_Apprehended"],
                              name="Apprehended", marker_color=COLORS["cbp_apprehended"]))
        fig2.add_trace(go.Bar(x=fdf["Date"], y=fdf["CBP_Transferred"],
                              name="Transferred to HHS", marker_color=COLORS["cbp_transfer"]))
        fig2.update_layout(barmode="overlay", height=300,
                           title="Apprehensions vs Transfers (CBP)")
        st.plotly_chart(fig2, use_container_width=True)

    with col2:
        st.markdown('<div class="section-header">Monthly Aggregate Flow</div>', unsafe_allow_html=True)
        monthly = fdf.groupby("Month").agg(
            Apprehended=("CBP_Apprehended","sum"),
            Transferred=("CBP_Transferred","sum"),
            Discharged=("HHS_Discharged","sum")
        ).reset_index()
        fig3 = go.Figure()
        fig3.add_trace(go.Bar(x=monthly["Month"], y=monthly["Apprehended"],
                              name="Apprehended", marker_color=COLORS["cbp_apprehended"]))
        fig3.add_trace(go.Bar(x=monthly["Month"], y=monthly["Transferred"],
                              name="Transferred", marker_color=COLORS["cbp_transfer"]))
        fig3.add_trace(go.Bar(x=monthly["Month"], y=monthly["Discharged"],
                              name="Discharged", marker_color=COLORS["hhs_discharged"]))
        fig3.update_layout(barmode="group", height=300, title="Monthly Flow Totals")
        st.plotly_chart(fig3, use_container_width=True)

# ── Tab 2: Efficiency Metrics ─────────────────
with tab2:
    st.markdown('<div class="section-header">Process Efficiency Ratios Over Time</div>', unsafe_allow_html=True)
    fig = go.Figure()
    if show_ter:
        fig.add_trace(go.Scatter(x=fdf["Date"], y=fdf["Transfer_Efficiency"],
                                 name="Transfer Efficiency Ratio", line=dict(color=COLORS["te"], width=1.5)))
    if show_dei:
        fig.add_trace(go.Scatter(x=fdf["Date"], y=fdf["Discharge_Effectiveness"],
                                 name="Discharge Effectiveness Index", line=dict(color=COLORS["dei"], width=1.5)))
    if show_pt:
        fig.add_trace(go.Scatter(x=fdf["Date"], y=fdf["Pipeline_Throughput"],
                                 name="Pipeline Throughput", line=dict(color=COLORS["pt"], width=1.5)))
    # alert lines
    fig.add_hline(y=te_thresh, line_dash="dot", line_color="#D64045",
                  annotation_text=f"Transfer Alert ({te_thresh:.0%})", annotation_position="bottom right")
    fig.update_layout(height=380, title="Efficiency Ratio Dashboard",
                      yaxis_title="Ratio / Index")
    st.plotly_chart(fig, use_container_width=True)

    col1, col2 = st.columns(2)
    with col1:
        # Rolling 30-day avg
        st.markdown('<div class="section-header">30-Day Rolling Transfer Efficiency</div>', unsafe_allow_html=True)
        roll = fdf["Transfer_Efficiency"].rolling(30, min_periods=1).mean()
        fig4 = go.Figure()
        fig4.add_trace(go.Scatter(x=fdf["Date"], y=fdf["Transfer_Efficiency"],
                                  name="Daily", line=dict(color=COLORS["te"], width=1), opacity=0.4))
        fig4.add_trace(go.Scatter(x=fdf["Date"], y=roll,
                                  name="30-day avg", line=dict(color=COLORS["te"], width=2.5)))
        fig4.update_layout(height=300, title="Transfer Efficiency — Smoothed")
        st.plotly_chart(fig4, use_container_width=True)

    with col2:
        st.markdown('<div class="section-header">Discharge Effectiveness Distribution</div>', unsafe_allow_html=True)
        fig5 = go.Figure()
        fig5.add_trace(go.Histogram(x=fdf["Discharge_Effectiveness"],
                                    marker_color=COLORS["dei"], nbinsx=40, opacity=0.8))
        fig5.update_layout(height=300, title="Distribution of Discharge Effectiveness",
                           xaxis_title="Discharge Effectiveness", yaxis_title="Count")
        st.plotly_chart(fig5, use_container_width=True)

# ── Tab 3: Bottleneck Detection ───────────────
with tab3:
    st.markdown('<div class="section-header">Backlog Accumulation & Delay Identification</div>', unsafe_allow_html=True)

    if show_back:
        fig = go.Figure()
        colors_back = [COLORS["backlog"] if v > 0 else COLORS["te"] for v in fdf["Backlog_Delta"]]
        fig.add_trace(go.Bar(x=fdf["Date"], y=fdf["Backlog_Delta"],
                             name="Backlog Delta (Apprehended − Transferred)",
                             marker_color=colors_back))
        fig.add_hline(y=0, line_color="#E8EDF2", line_width=1)
        fig.update_layout(height=350, title="Daily Backlog Accumulation (red = buildup, teal = release)",
                          yaxis_title="Δ Children")
        st.plotly_chart(fig, use_container_width=True)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<div class="section-header">Monthly Net Flow (Entries vs Exits)</div>', unsafe_allow_html=True)
        monthly2 = fdf.groupby("Month").agg(
            Entries=("CBP_Apprehended","sum"),
            Exits=("HHS_Discharged","sum")
        ).reset_index()
        monthly2["Net"] = monthly2["Exits"] - monthly2["Entries"]
        fig6 = go.Figure()
        fig6.add_trace(go.Bar(x=monthly2["Month"], y=monthly2["Entries"],
                              name="Entries (Apprehended)", marker_color=COLORS["cbp_apprehended"]))
        fig6.add_trace(go.Bar(x=monthly2["Month"], y=monthly2["Exits"],
                              name="Exits (Discharged)", marker_color=COLORS["hhs_discharged"]))
        fig6.update_layout(barmode="group", height=320, title="Monthly Inflow vs Outflow")
        st.plotly_chart(fig6, use_container_width=True)

    with col2:
        st.markdown('<div class="section-header">High-Backlog Days Table</div>', unsafe_allow_html=True)
        threshold = fdf["Backlog_Delta"].quantile(0.90)
        bottleneck_df = fdf[fdf["Backlog_Delta"] > threshold][
            ["Date","CBP_Apprehended","CBP_Transferred","Backlog_Delta","Transfer_Efficiency"]
        ].sort_values("Backlog_Delta", ascending=False).head(15)
        bottleneck_df["Date"] = bottleneck_df["Date"].dt.strftime("%b %d, %Y")
        bottleneck_df["Transfer_Efficiency"] = bottleneck_df["Transfer_Efficiency"].apply(lambda x: f"{x:.1%}")
        st.dataframe(bottleneck_df.rename(columns={
            "Date":"Date","CBP_Apprehended":"Apprehended",
            "CBP_Transferred":"Transferred","Backlog_Delta":"Backlog","Transfer_Efficiency":"TER"
        }), use_container_width=True, hide_index=True)

# ── Tab 4: Outcome Trends ─────────────────────
with tab4:
    st.markdown('<div class="section-header">Sponsor Placement Outcome Analysis</div>', unsafe_allow_html=True)

    col1, col2 = st.columns([2,1])
    with col1:
        fig7 = make_subplots(rows=2, cols=1, shared_xaxes=True,
                             subplot_titles=["HHS Census", "Daily Discharges"])
        fig7.add_trace(go.Scatter(x=fdf["Date"], y=fdf["HHS_Care"],
                                  fill="tozeroy", fillcolor="rgba(214,64,69,0.10)",
                                  line=dict(color=COLORS["hhs_care"], width=2),
                                  name="HHS Census"), row=1, col=1)
        fig7.add_trace(go.Bar(x=fdf["Date"], y=fdf["HHS_Discharged"],
                              marker_color=COLORS["hhs_discharged"], name="Daily Discharges",
                              opacity=0.8), row=2, col=1)
        roll_dis = fdf["HHS_Discharged"].rolling(14, min_periods=1).mean()
        fig7.add_trace(go.Scatter(x=fdf["Date"], y=roll_dis,
                                  line=dict(color="#E8A838", width=2),
                                  name="14-day avg discharges"), row=2, col=1)
        fig7.update_layout(height=420, showlegend=True,
                           title="HHS Population & Discharge Performance")
        for ax in ["xaxis2","yaxis","yaxis2"]:
            fig7.update_layout(**{ax: dict(gridcolor="#1B3A5C", linecolor="#1B3A5C")})
        st.plotly_chart(fig7, use_container_width=True)

    with col2:
        st.markdown('<div class="section-header">Outcome Stability Score</div>', unsafe_allow_html=True)
        fig8 = go.Figure()
        fig8.add_trace(go.Scatter(x=fdf["Date"], y=fdf["Outcome_Stability"],
                                  fill="tozeroy", fillcolor="rgba(155,93,229,0.15)",
                                  line=dict(color="#9B5DE5", width=1.5),
                                  name="Std Dev (7-day rolling)"))
        fig8.update_layout(height=200, title="Placement Variability",
                           margin=dict(l=40,r=20,t=40,b=20))
        st.plotly_chart(fig8, use_container_width=True)

        # Summary stats
        st.markdown('<div class="section-header">Discharge Summary</div>', unsafe_allow_html=True)
        st.metric("Total Discharges", f"{int(fdf['HHS_Discharged'].sum()):,}")
        st.metric("Peak Day",         f"{int(fdf['HHS_Discharged'].max()):,}")
        st.metric("Avg/Day",          f"{fdf['HHS_Discharged'].mean():.0f}")
        st.metric("Days with 0",      f"{(fdf['HHS_Discharged']==0).sum()}")

    # Month-over-month
    st.markdown('<div class="section-header">Month-over-Month Placement Trends</div>', unsafe_allow_html=True)
    mom = fdf.groupby("Month").agg(
        Avg_Discharged=("HHS_Discharged","mean"),
        Avg_HHS=("HHS_Care","mean"),
        Avg_DEI=("Discharge_Effectiveness","mean")
    ).reset_index()
    fig9 = go.Figure()
    fig9.add_trace(go.Scatter(x=mom["Month"], y=mom["Avg_Discharged"],
                              name="Avg Daily Discharges", line=dict(color=COLORS["hhs_discharged"], width=2),
                              mode="lines+markers"))
    fig9.add_trace(go.Scatter(x=mom["Month"], y=mom["Avg_DEI"]*1000,
                              name="Avg DEI ×1000", line=dict(color=COLORS["dei"], width=2, dash="dot"),
                              mode="lines+markers"))
    fig9.update_layout(height=310, title="Month-over-Month Outcome Trends",
                       yaxis_title="Value")
    st.plotly_chart(fig9, use_container_width=True)

# ── Tab 5: Temporal Patterns ──────────────────
with tab5:
    st.markdown('<div class="section-header">Weekday vs Weekend Analysis</div>', unsafe_allow_html=True)

    dow_order = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]
    dow = fdf.groupby("DayOfWeek").agg(
        Avg_Transferred=("CBP_Transferred","mean"),
        Avg_Discharged=("HHS_Discharged","mean"),
        Avg_TE=("Transfer_Efficiency","mean"),
    ).reindex(dow_order).reset_index()

    col1, col2 = st.columns(2)
    with col1:
        fig10 = go.Figure()
        fig10.add_trace(go.Bar(x=dow["DayOfWeek"], y=dow["Avg_Transferred"],
                               name="Avg Transfers", marker_color=COLORS["cbp_transfer"]))
        fig10.add_trace(go.Bar(x=dow["DayOfWeek"], y=dow["Avg_Discharged"],
                               name="Avg Discharges", marker_color=COLORS["hhs_discharged"]))
        fig10.update_layout(height=320, barmode="group",
                            title="Average Daily Activity by Day of Week")
        st.plotly_chart(fig10, use_container_width=True)

    with col2:
        fig11 = go.Figure()
        bar_colors = ["#2E86AB" if d not in ["Saturday","Sunday"] else "#D64045" for d in dow["DayOfWeek"]]
        fig11.add_trace(go.Bar(x=dow["DayOfWeek"], y=dow["Avg_TE"],
                               name="Avg Transfer Efficiency",
                               marker_color=bar_colors))
        fig11.update_layout(height=320, title="Transfer Efficiency by Day (red = weekend)")
        st.plotly_chart(fig11, use_container_width=True)

    st.markdown('<div class="section-header">Monthly Trend Summary</div>', unsafe_allow_html=True)
    monthly_summary = fdf.groupby("Month").agg(
        Avg_TE=("Transfer_Efficiency","mean"),
        Avg_DEI=("Discharge_Effectiveness","mean"),
        Total_Apprehended=("CBP_Apprehended","sum"),
        Total_Discharged=("HHS_Discharged","sum"),
        Max_HHS=("HHS_Care","max"),
        Min_HHS=("HHS_Care","min"),
    ).reset_index()

    fig12 = go.Figure()
    fig12.add_trace(go.Scatter(x=monthly_summary["Month"],
                               y=monthly_summary["Avg_TE"],
                               name="Avg Transfer Efficiency",
                               line=dict(color=COLORS["te"], width=2),
                               mode="lines+markers"))
    fig12.add_trace(go.Scatter(x=monthly_summary["Month"],
                               y=monthly_summary["Avg_DEI"],
                               name="Avg Discharge Effectiveness",
                               line=dict(color=COLORS["dei"], width=2, dash="dot"),
                               mode="lines+markers",
                               yaxis="y2"))
    fig12.update_layout(height=350, title="Monthly Efficiency Overview",
                        yaxis=dict(title="Transfer Efficiency", gridcolor="#1B3A5C", linecolor="#1B3A5C"),
                        yaxis2=dict(title="Discharge Effectiveness", overlaying="y", side="right",
                                    gridcolor="rgba(0,0,0,0)", linecolor="#1B3A5C"))
    st.plotly_chart(fig12, use_container_width=True)

    # Heatmap: month × day-of-week discharge
    st.markdown('<div class="section-header">Discharge Activity Heatmap</div>', unsafe_allow_html=True)
    fdf["MonthName"] = fdf["Date"].dt.strftime("%Y-%m")
    heat = fdf.groupby(["MonthName","DayOfWeek"])["HHS_Discharged"].mean().unstack(fill_value=0)
    heat = heat.reindex(columns=[d for d in dow_order if d in heat.columns])
    months_sorted = sorted(heat.index.tolist())
    heat = heat.loc[months_sorted]

    fig13 = go.Figure(go.Heatmap(
        z=heat.values,
        x=heat.columns.tolist(),
        y=heat.index.tolist(),
        colorscale=[[0,"#0D1B2A"],[0.5,"#2E86AB"],[1,"#3BCEAC"]],
        hovertemplate="Month: %{y}<br>Day: %{x}<br>Avg Discharges: %{z:.1f}<extra></extra>"
    ))
    fig13.update_layout(height=400, title="Average Daily Discharges — Month × Weekday",
                        xaxis_title="Day of Week", yaxis_title="Month")
    st.plotly_chart(fig13, use_container_width=True)

# ─────────────────────────────────────────────
# FOOTER
# ─────────────────────────────────────────────
st.markdown("---")
st.markdown("""
<div style="text-align:center; color:#8FA5BA; font-size:0.75rem; padding:0.5rem 0 1rem 0;">
    UAC Care Transition Analytics · ShadowFox AIML Internship Project ·
    Data Source: HHS/ORR Reporting
</div>
""", unsafe_allow_html=True)