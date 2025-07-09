import streamlit as st
import streamlit.components.v1 as components
from examples import PREDEFINED_QUERIES
from llm_cypher import nl_to_cypher, results_to_nl
from neo4j_utils import connect_neo4j, run_cypher
from visualization import render_graph
from logs import log_reasoning

st.set_page_config(
    page_title="CrimeSys",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
body, .stApp {
    background-color: #181a20 !important;
    color: #f8f9fa !important;
}
.main-header {
    font-size: 2.5rem;
    font-weight: 300;
    text-align: center;
    margin-bottom: 2rem;
    color: #f8f9fa;
}
.subtitle {
    text-align: center;
    color: #b0b3b8;
    margin-bottom: 3rem;
    font-size: 1.1rem;
}
.query-input {
    background: #23272f;
    border: 2px solid #23272f;
    border-radius: 12px;
    padding: 1rem;
    margin-bottom: 1rem;
}
[data-testid="stTextInput"] > div > input {
    background-color: #23272f !important;
    color: #f8f9fa !important;
    border-radius: 10px !important;
    border: 1.5px solid #444 !important;
    font-size: 1.1rem !important;
    padding: 0.75rem 1rem !important;
    box-shadow: none !important;
}
.answer-box {
    background: #23272f;
    border: 1px solid #333;
    border-radius: 12px;
    padding: 1.5rem;
    margin: 1.5rem 0 2rem 0;
    box-shadow: 0 2px 8px rgba(0,0,0,0.25);
    animation: fadeIn 1.2s cubic-bezier(.39,.575,.565,1) both;
}
@keyframes fadeIn {
    0% { opacity: 0; transform: translateY(30px); }
    100% { opacity: 1; transform: translateY(0); }
}
.example-btn {
    background: #23272f;
    border: 1px solid #444;
    border-radius: 8px;
    padding: 0.5rem 1rem;
    margin: 0.25rem;
    font-size: 0.9rem;
    color: #f8f9fa;
    transition: background 0.2s, color 0.2s;
}
.example-btn:hover {
    background: #333;
    color: #fff;
}
.log-section {
    background: #23272f;
    border-radius: 8px;
    padding: 1rem;
    font-family: 'Courier New', monospace;
    font-size: 0.85rem;
    color: #b0b3b8;
}
.metric-card {
    background: #23272f;
    border: 1px solid #333;
    border-radius: 8px;
    padding: 1rem;
    text-align: center;
    margin: 0.5rem;
    color: #f8f9fa;
}
.metric-value {
    font-size: 1.5rem;
    font-weight: bold;
    color: #00bfff;
}
.metric-label {
    font-size: 0.9rem;
    color: #b0b3b8;
}
.stButton > button {
    background: #ff4b4b;
    color: #fff;
    border-radius: 8px;
    border: none;
    font-size: 1.1rem;
    padding: 0.6rem 1.2rem;
    margin: 0.2rem 0.2rem 0.2rem 0;
    transition: background 0.2s;
}
.stButton > button:hover {
    background: #ff6b6b;
    color: #fff;
}
.st-bb, .st-cq, .st-cp, .st-cq, .st-cv, .st-cw, .st-cx, .st-cy, .st-cz, .st-da, .st-db, .st-dc, .st-dd, .st-de, .st-df, .st-dg, .st-dh, .st-di, .st-dj, .st-dk, .st-dl, .st-dm, .st-dn, .st-do, .st-dp, .st-dq, .st-dr, .st-ds, .st-dt, .st-du, .st-dv, .st-dw, .st-dx, .st-dy, .st-dz, .st-e0, .st-e1, .st-e2, .st-e3, .st-e4, .st-e5, .st-e6, .st-e7, .st-e8, .st-e9, .st-ea, .st-eb, .st-ec, .st-ed, .st-ee, .st-ef, .st-eg, .st-eh, .st-ei, .st-ej, .st-ek, .st-el, .st-em, .st-en, .st-eo, .st-ep, .st-eq, .st-er, .st-es, .st-et, .st-eu, .st-ev, .st-ew, .st-ex, .st-ey, .st-ez, .st-f0, .st-f1, .st-f2, .st-f3, .st-f4, .st-f5, .st-f6, .st-f7, .st-f8, .st-f9, .st-fa, .st-fb, .st-fc, .st-fd, .st-fe, .st-ff, .st-fg, .st-fh, .st-fi, .st-fj, .st-fk, .st-fl, .st-fm, .st-fn, .st-fo, .st-fp, .st-fq, .st-fr, .st-fs, .st-ft, .st-fu, .st-fv, .st-fw, .st-fx, .st-fy, .st-fz, .st-g0, .st-g1, .st-g2, .st-g3, .st-g4, .st-g5, .st-g6, .st-g7, .st-g8, .st-g9, .st-ga, .st-gb, .st-gc, .st-gd, .st-ge, .st-gf, .st-gg, .st-gh, .st-gi, .st-gj, .st-gk, .st-gl, .st-gm, .st-gn, .st-go, .st-gp, .st-gq, .st-gr, .st-gs, .st-gt, .st-gu, .st-gv, .st-gw, .st-gx, .st-gy, .st-gz, .st-h0, .st-h1, .st-h2, .st-h3, .st-h4, .st-h5, .st-h6, .st-h7, .st-h8, .st-h9, .st-ha, .st-hb, .st-hc, .st-hd, .st-he, .st-hf, .st-hg, .st-hh, .st-hi, .st-hj, .st-hk, .st-hl, .st-hm, .st-hn, .st-ho, .st-hp, .st-hq, .st-hr, .st-hs, .st-ht, .st-hu, .st-hv, .st-hw, .st-hx, .st-hy, .st-hz, .st-i0, .st-i1, .st-i2, .st-i3, .st-i4, .st-i5, .st-i6, .st-i7, .st-i8, .st-i9, .st-ia, .st-ib, .st-ic, .st-id, .st-ie, .st-if, .st-ig, .st-ih, .st-ii, .st-ij, .st-ik, .st-il, .st-im, .st-in, .st-io, .st-ip, .st-iq, .st-ir, .st-is, .st-it, .st-iu, .st-iv, .st-iw, .st-ix, .st-iy, .st-iz, .st-j0, .st-j1, .st-j2, .st-j3, .st-j4, .st-j5, .st-j6, .st-j7, .st-j8, .st-j9, .st-ja, .st-jb, .st-jc, .st-jd, .st-je, .st-jf, .st-jg, .st-jh, .st-ji, .st-jj, .st-jk, .st-jl, .st-jm, .st-jn, .st-jo, .st-jp, .st-jq, .st-jr, .st-js, .st-jt, .st-ju, .st-jv, .st-jw, .st-jx, .st-jy, .st-jz, .st-k0, .st-k1, .st-k2, .st-k3, .st-k4, .st-k5, .st-k6, .st-k7, .st-k8, .st-k9, .st-ka, .st-kb, .st-kc, .st-kd, .st-ke, .st-kf, .st-kg, .st-kh, .st-ki, .st-kj, .st-kk, .st-kl, .st-km, .st-kn, .st-ko, .st-kp, .st-kq, .st-kr, .st-ks, .st-kt, .st-ku, .st-kv, .st-kw, .st-kx, .st-ky, .st-kz, .st-l0, .st-l1, .st-l2, .st-l3, .st-l4, .st-l5, .st-l6, .st-l7, .st-l8, .st-l9, .st-la, .st-lb, .st-lc, .st-ld, .st-le, .st-lf, .st-lg, .st-lh, .st-li, .st-lj, .st-lk, .st-ll, .st-lm, .st-ln, .st-lo, .st-lp, .st-lq, .st-lr, .st-ls, .st-lt, .st-lu, .st-lv, .st-lw, .st-lx, .st-ly, .st-lz, .st-m0, .st-m1, .st-m2, .st-m3, .st-m4, .st-m5, .st-m6, .st-m7, .st-m8, .st-m9, .st-ma, .st-mb, .st-mc, .st-md, .st-me, .st-mf, .st-mg, .st-mh, .st-mi, .st-mj, .st-mk, .st-ml, .st-mm, .st-mn, .st-mo, .st-mp, .st-mq, .st-mr, .st-ms, .st-mt, .st-mu, .st-mv, .st-mw, .st-mx, .st-my, .st-mz, .st-n0, .st-n1, .st-n2, .st-n3, .st-n4, .st-n5, .st-n6, .st-n7, .st-n8, .st-n9, .st-na, .st-nb, .st-nc, .st-nd, .st-ne, .st-nf, .st-ng, .st-nh, .st-ni, .st-nj, .st-nk, .st-nl, .st-nm, .st-nn, .st-no, .st-np, .st-nq, .st-nr, .st-ns, .st-nt, .st-nu, .st-nv, .st-nw, .st-nx, .st-ny, .st-nz, .st-o0, .st-o1, .st-o2, .st-o3, .st-o4, .st-o5, .st-o6, .st-o7, .st-o8, .st-o9, .st-oa, .st-ob, .st-oc, .st-od, .st-oe, .st-of, .st-og, .st-oh, .st-oi, .st-oj, .st-ok, .st-ol, .st-om, .st-on, .st-oo, .st-op, .st-oq, .st-or, .st-os, .st-ot, .st-ou, .st-ov, .st-ow, .st-ox, .st-oy, .st-oz, .st-p0, .st-p1, .st-p2, .st-p3, .st-p4, .st-p5, .st-p6, .st-p7, .st-p8, .st-p9, .st-pa, .st-pb, .st-pc, .st-pd, .st-pe, .st-pf, .st-pg, .st-ph, .st-pi, .st-pj, .st-pk, .st-pl, .st-pm, .st-pn, .st-po, .st-pp, .st-pq, .st-pr, .st-ps, .st-pt, .st-pu, .st-pv, .st-pw, .st-px, .st-py, .st-pz, .st-q0, .st-q1, .st-q2, .st-q3, .st-q4, .st-q5, .st-q6, .st-q7, .st-q8, .st-q9, .st-qa, .st-qb, .st-qc, .st-qd, .st-qe, .st-qf, .st-qg, .st-qh, .st-qi, .st-qj, .st-qk, .st-ql, .st-qm, .st-qn, .st-qo, .st-qp, .st-qq, .st-qr, .st-qs, .st-qt, .st-qu, .st-qv, .st-qw, .st-qx, .st-qy, .st-qz, .st-r0, .st-r1, .st-r2, .st-r3, .st-r4, .st-r5, .st-r6, .st-r7, .st-r8, .st-r9, .st-ra, .st-rb, .st-rc, .st-rd, .st-re, .st-rf, .st-rg, .st-rh, .st-ri, .st-rj, .st-rk, .st-rl, .st-rm, .st-rn, .st-ro, .st-rp, .st-rq, .st-rr, .st-rs, .st-rt, .st-ru, .st-rv, .st-rw, .st-rx, .st-ry, .st-rz, .st-s0, .st-s1, .st-s2, .st-s3, .st-s4, .st-s5, .st-s6, .st-s7, .st-s8, .st-s9, .st-sa, .st-sb, .st-sc, .st-sd, .st-se, .st-sf, .st-sg, .st-sh, .st-si, .st-sj, .st-sk, .st-sl, .st-sm, .st-sn, .st-so, .st-sp, .st-sq, .st-sr, .st-ss, .st-st, .st-su, .st-sv, .st-sw, .st-sx, .st-sy, .st-sz, .st-t0, .st-t1, .st-t2, .st-t3, .st-t4, .st-t5, .st-t6, .st-t7, .st-t8, .st-t9, .st-ta, .st-tb, .st-tc, .st-td, .st-te, .st-tf, .st-tg, .st-th, .st-ti, .st-tj, .st-tk, .st-tl, .st-tm, .st-tn, .st-to, .st-tp, .st-tq, .st-tr, .st-ts, .st-tt, .st-tu, .st-tv, .st-tw, .st-tx, .st-ty, .st-tz, .st-u0, .st-u1, .st-u2, .st-u3, .st-u4, .st-u5, .st-u6, .st-u7, .st-u8, .st-u9, .st-ua, .st-ub, .st-uc, .st-ud, .st-ue, .st-uf, .st-ug, .st-uh, .st-ui, .st-uj, .st-uk, .st-ul, .st-um, .st-un, .st-uo, .st-up, .st-uq, .st-ur, .st-us, .st-ut, .st-uu, .st-uv, .st-uw, .st-ux, .st-uy, .st-uz, .st-v0, .st-v1, .st-v2, .st-v3, .st-v4, .st-v5, .st-v6, .st-v7, .st-v8, .st-v9, .st-va, .st-vb, .st-vc, .st-vd, .st-ve, .st-vf, .st-vg, .st-vh, .st-vi, .st-vj, .st-vk, .st-vl, .st-vm, .st-vn, .st-vo, .st-vp, .st-vq, .st-vr, .st-vs, .st-vt, .st-vu, .st-vv, .st-vw, .st-vx, .st-vy, .st-vz, .st-w0, .st-w1, .st-w2, .st-w3, .st-w4, .st-w5, .st-w6, .st-w7, .st-w8, .st-w9, .st-wa, .st-wb, .st-wc, .st-wd, .st-we, .st-wf, .st-wg, .st-wh, .st-wi, .st-wj, .st-wk, .st-wl, .st-wm, .st-wn, .st-wo, .st-wp, .st-wq, .st-wr, .st-ws, .st-wt, .st-wu, .st-wv, .st-ww, .st-wx, .st-wy, .st-wz, .st-x0, .st-x1, .st-x2, .st-x3, .st-x4, .st-x5, .st-x6, .st-x7, .st-x8, .st-x9, .st-xa, .st-xb, .st-xc, .st-xd, .st-xe, .st-xf, .st-xg, .st-xh, .st-xi, .st-xj, .st-xk, .st-xl, .st-xm, .st-xn, .st-xo, .st-xp, .st-xq, .st-xr, .st-xs, .st-xt, .st-xu, .st-xv, .st-xw, .st-xx, .st-xy, .st-xz, .st-y0, .st-y1, .st-y2, .st-y3, .st-y4, .st-y5, .st-y6, .st-y7, .st-y8, .st-y9, .st-ya, .st-yb, .st-yc, .st-yd, .st-ye, .st-yf, .st-yg, .st-yh, .st-yi, .st-yj, .st-yk, .st-yl, .st-ym, .st-yn, .st-yo, .st-yp, .st-yq, .st-yr, .st-ys, .st-yt, .st-yu, .st-yv, .st-yw, .st-yx, .st-yy, .st-yz, .st-z0, .st-z1, .st-z2, .st-z3, .st-z4, .st-z5, .st-z6, .st-z7, .st-z8, .st-z9, .st-za, .st-zb, .st-zc, .st-zd, .st-ze, .st-zf, .st-zg, .st-zh, .st-zi, .st-zj, .st-zk, .st-zl, .st-zm, .st-zn, .st-zo, .st-zp, .st-zq, .st-zr, .st-zs, .st-zt, .st-zu, .st-zv, .st-zw, .st-zx, .st-zy, .st-zz {
    background: #181a20 !important;
    color: #f8f9fa !important;
}
</style>
""", unsafe_allow_html=True)

if 'query' not in st.session_state:
    st.session_state['query'] = ''
if 'cypher' not in st.session_state:
    st.session_state['cypher'] = ''
if 'results' not in st.session_state:
    st.session_state['results'] = None
if 'logs' not in st.session_state:
    st.session_state['logs'] = []
if 'nl_answer' not in st.session_state:
    st.session_state['nl_answer'] = ''

st.markdown('<h1 class="main-header">CrimeSys</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">AI-powered crime investigation using knowledge graphs</p>', unsafe_allow_html=True)

col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    st.markdown('<div class="query-input">', unsafe_allow_html=True)
    user_query = st.text_input(
        "Ask about crimes, people, locations, or relationships...",
        value=st.session_state['query'],
        key="query_input",
        help="Try: 'Find people involved in multiple crimes' or 'What locations have the highest crime rate?'"
    )
    st.markdown('</div>', unsafe_allow_html=True)
    
    col_btn1, col_btn2 = st.columns([1, 1])
    with col_btn1:
        ask_clicked = st.button("🔍 Ask", use_container_width=True, type="primary")
    with col_btn2:
        if st.button("🔄 Clear", use_container_width=True):
            st.session_state['query'] = ''
            st.session_state['results'] = None
            st.session_state['nl_answer'] = ''
            st.session_state['logs'] = []
            st.rerun()
    
    st.markdown("**Try these examples:**")
    example_cols = st.columns(3)
    for i, q in enumerate(PREDEFINED_QUERIES):
        with example_cols[i % 3]:
            if st.button(q, key=f"example_{i}", use_container_width=True):
                st.session_state['query'] = q
                user_query = q
                ask_clicked = True

if ask_clicked and user_query:
    st.session_state['logs'] = []
    log = lambda msg: st.session_state['logs'].append(msg)
    log(f"Processing: {user_query}")
    
    with st.spinner("Generating Cypher query..."):
        cypher = nl_to_cypher(user_query)
        st.session_state['cypher'] = cypher
        log(f"Generated Cypher: {cypher}")
    
    with st.spinner("Querying Neo4j..."):
        try:
            driver = connect_neo4j()
            results = run_cypher(driver, cypher)
            if driver:
                driver.close()
            st.session_state['results'] = results
            log(f"Found {len(results)} results")
        except Exception as e:
            results = None
            log(f"Neo4j error: {e}")
            st.session_state['results'] = None
    
    if results:
        with st.spinner("Generating answer..."):
            try:
                nl_answer = results_to_nl(user_query, cypher, results)
                st.session_state['nl_answer'] = nl_answer
            except Exception as e:
                st.session_state['nl_answer'] = f"Found {len(results)} results, but could not generate a summary."
    
    st.success("Analysis complete!")

if st.session_state['nl_answer'] or st.session_state['results']:
    st.markdown("---")
    
    if st.session_state['results']:
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{len(st.session_state['results'])}</div>
                <div class="metric-label">Results</div>
            </div>
            """, unsafe_allow_html=True)
        with col2:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{len(st.session_state['cypher'].split())}</div>
                <div class="metric-label">Query Words</div>
            </div>
            """, unsafe_allow_html=True)
        with col3:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{len(st.session_state['logs'])}</div>
                <div class="metric-label">Steps</div>
            </div>
            """, unsafe_allow_html=True)
    
    if st.session_state['nl_answer']:
        st.markdown('<div class="answer-box">', unsafe_allow_html=True)
        st.markdown("### Answer")
        st.markdown(st.session_state['nl_answer'])
        st.markdown('</div>', unsafe_allow_html=True)
    
    if st.session_state['results']:
        st.markdown("### Graph Visualization")
        try:
            html_graph = render_graph(st.session_state['results'])
            if html_graph:
                components.html(html_graph, height=500, scrolling=True)
            else:
                st.info("No graph data to visualize. Try a query that returns nodes or relationships.")
        except Exception as e:
            st.error(f"Graph visualization error: {e}")
    
    with st.expander("Technical Details"):
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**Generated Cypher:**")
            st.code(st.session_state['cypher'], language="cypher")
        with col2:
            st.markdown("**Processing Log:**")
            st.markdown('<div class="log-section">', unsafe_allow_html=True)
            for log_entry in st.session_state['logs']:
                st.text(log_entry)
            st.markdown('</div>', unsafe_allow_html=True)

with st.sidebar:
    st.markdown("### About")
    st.markdown("""
    This system uses:
    - **Neo4j** for the knowledge graph
    - **LLaMA 3** for natural language processing
    - **POLE dataset** for crime data
    """)
    
    st.markdown("### Tips")
    st.markdown("""
    - Ask about people, crimes, locations
    - Use specific details for better results
    - Try the example queries to get started
    """)

st.markdown("---")
st.markdown("<p style='text-align: center; color: #666;'>CrimeSys - AI-powered crime investigation system, Built by Deeraj</p>", unsafe_allow_html=True) 