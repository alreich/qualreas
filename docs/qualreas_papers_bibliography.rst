Annotated Bibliography
======================

This is an annotated bibliography of 66 works on qualitative temporal
and spatial reasoning with relation algebras: Allen’s interval algebra
and its relatives, point and interval calculi, the Region Connection
Calculus, and the constraint-based methods used to reason with them.

The ``qualreas`` package is based on A. J. Reich’s 1994 paper,
*Intervals, Points, and Branching Time* (entry **[C3]**), which extends
Allen’s algebra with points and branching time.

The works are grouped into nine subtopics (Section 1) and, within each
group, sorted by publication date from earliest to latest (Section 3).
Section 4 lists all of them in a single chronological table. Dates are
the years of formal publication; where a work first circulated as a
draft or technical report, or exists in several versions, the entry says
so and cites the published one.

1. Categories
-------------

+-----------------------+--------------------------------------------------------------------+-----------------------+
|                       | Category                                                           | Works                 |
+=======================+====================================================================+=======================+
| **A**                 | `Allen Interval Algebra Foundations and                            | 15                    |
|                       | Complexity <#Allen-Interval-Algebra-Foundations-and-Complexity>`__ |                       |
+-----------------------+--------------------------------------------------------------------+-----------------------+
| **B**                 | `Metric and Disjunctive Temporal                                   | 4                     |
|                       | Constraints <#Metric-and-Disjunctive-Temporal-Constraints>`__      |                       |
+-----------------------+--------------------------------------------------------------------+-----------------------+
| **C**                 | `Extensions of the Interval                                        | 6                     |
|                       | Algebra <#Extensions-of-the-Interval-Algebra>`__                   |                       |
+-----------------------+--------------------------------------------------------------------+-----------------------+
| **D**                 | `Relation Algebras and Time                                        | 8                     |
|                       | Ontologies <#Relation-Algebras-and-Time-Ontologies>`__             |                       |
+-----------------------+--------------------------------------------------------------------+-----------------------+
| **E**                 | `Qualitative Spatial Reasoning <#Qualitative-Spatial-Reasoning>`__ | 9                     |
+-----------------------+--------------------------------------------------------------------+-----------------------+
| **F**                 | `Software and Implementations <#Software-and-Implementations>`__   | 8                     |
+-----------------------+--------------------------------------------------------------------+-----------------------+
| **G**                 | `Applications and Cognitive                                        | 5                     |
|                       | Studies <#Applications-and-Cognitive-Studies>`__                   |                       |
+-----------------------+--------------------------------------------------------------------+-----------------------+
| **H**                 | `Temporal Reasoning in Natural Language                            | 4                     |
|                       | Processing <#Temporal-Reasoning-in-Natural-Language-Processing>`__ |                       |
+-----------------------+--------------------------------------------------------------------+-----------------------+
| **I**                 | `Surveys and Overviews <#Surveys-and-Overviews>`__                 | 7                     |
+-----------------------+--------------------------------------------------------------------+-----------------------+
|                       | **Total**                                                          | **66**                |
+-----------------------+--------------------------------------------------------------------+-----------------------+

Category **I** (surveys) is a form of publication rather than a subject,
so it cuts across the others; each survey is listed there rather than
under its topic. Each work appears in exactly one category.

2. About the Links
------------------

- 🟢 **free full text** (PDF or open-access page)
- 🔒 **publisher or DOI page** (may require a subscription)
- 📄 **catalog or record page** (the paper may not be downloadable
  there)
- **†** marks a link that could not be opened when this list was
  compiled. It was taken from a search result or from an index page that
  lists it, so check it before relying on it.

DOIs were taken from publisher or repository pages but not individually
resolved. For the Elsevier *Artificial Intelligence* papers only the DOI
was found, so check whether ScienceDirect offers free access. Where
several versions exist (technical report, preprint, journal), the free
one is labeled as such, and it may differ from the published text.

Some works have no online copy that could be found; they are marked *No
online copy found*.

3. Annotated Entries by Category
--------------------------------

Allen Interval Algebra Foundations and Complexity
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The core of the collection: Allen’s interval calculus and the
Vilain-Kautz point algebra, path-consistency and other propagation
algorithms, NP-completeness, and the search for tractable subclasses
(ORD-Horn and the maximal tractable subalgebras), through to a modern
ASP encoding.

| **[A1]** Vilain, M. B. (1982). A system for reasoning about time. In
  *Proceedings of the Second National Conference on Artificial
  Intelligence (AAAI-82)* (pp. 197–201). AAAI.
| 🟢 `PDF† <https://cdn.aaai.org/AAAI/1982/AAAI82-047.pdf>`__  ·  📄 `ML
  Anthology
  record <https://mlanthology.org/aaai/1982/vilain1982aaai-system>`__

| **[A2]** Allen, J. F. (1983). Maintaining knowledge about temporal
  intervals. *Communications of the ACM, 26*\ (11), 832–843.
| 🔒 `ACM (DOI; free access) <https://dx.doi.org/10.1145/182.358434>`__
   ·  🟢 `university-hosted
  PDF† <https://cse.unl.edu/~choueiry/Documents/Allen-CACM1983.pdf>`__

| **[A3]** Vilain, M., & Kautz, H. (1986). Constraint propagation
  algorithms for temporal reasoning. In *Proceedings of the Fifth
  National Conference on Artificial Intelligence (AAAI-86)*
  (pp. 377–382). AAAI.
| 🟢 `PDF† <https://cdn.aaai.org/AAAI/1986/AAAI86-063.pdf>`__  ·  📄 `ML
  Anthology
  record <https://mlanthology.org/aaai/1986/vilain1986aaai-constraint>`__

| **[A4]** Tsang, E. P. K. (1987). The consistent labeling problem in
  temporal reasoning. In *Proceedings of the Sixth National Conference
  on Artificial Intelligence (AAAI-87)* (pp. 251–255). AAAI.
| 🟢 `PDF† <https://cdn.aaai.org/AAAI/1987/AAAI87-045.pdf>`__  ·  📄 `ML
  Anthology
  record <https://mlanthology.org/aaai/1987/tsang1987aaai-consistent>`__

| **[A5]** van Beek, P. (1989). Approximation algorithms for temporal
  reasoning. In *Proceedings of the Eleventh International Joint
  Conference on Artificial Intelligence (IJCAI-89)* (pp. 1291–1296).
  Detroit.
| 🟢 `author’s
  PDF <https://cs.uwaterloo.ca/~vanbeek/Publications/ijcai89.pdf>`__  · 
  📄 `ML Anthology
  record <https://mlanthology.org/ijcai/1989/vanbeek1989ijcai-approximation>`__

| **[A6]** Vilain, M., Kautz, H., & van Beek, P. (1990). Constraint
  propagation algorithms for temporal reasoning: A revised report. In D.
  S. Weld & J. de Kleer (Eds.), *Readings in Qualitative Reasoning about
  Physical Systems* (pp. 373–381). Morgan Kaufmann.
| 🟢 `author’s
  PDF <https://cs.uwaterloo.ca/~vanbeek/Publications/VKvB89.pdf>`__  · 
  📄 `author’s
  page <https://cs.uwaterloo.ca/~vanbeek/Publications/qr_abs.html>`__
| Note: A revised and expanded version of the 1986 AAAI paper above (it
  cites work through 1989). van Beek’s page dates it 1989; it is cited
  here as the 1990 book chapter.

| **[A7]** van Beek, P., & Cohen, R. (1990). Exact and approximate
  reasoning about temporal relations. *Computational Intelligence, 6*,
  132–144.
| 🟢 `author’s
  PDF <https://cs.uwaterloo.ca/~vanbeek/Publications/ci90.pdf>`__  ·  📄
  `author’s
  page <https://cs.uwaterloo.ca/~vanbeek/Publications/ci90_abs.html>`__

| **[A8]** van Beek, P. (1992). Reasoning about qualitative temporal
  information. *Artificial Intelligence, 58*\ (1–3), 297–326.
| 🟢 `author’s
  PDF <https://cs.uwaterloo.ca/~vanbeek/Publications/ai92.pdf>`__  ·  🔒
  `publisher (DOI) <https://doi.org/10.1016/0004-3702%2892%2990011-L>`__
   ·  🟢 `workshop version
  (PDF)† <https://www.qrg.northwestern.edu/papers/Files/qr-workshops/QP90/vanBeek_Reasoning_Qualitative_Temporal_Information.pdf>`__
| Note: A preliminary version appeared at AAAI-90 (pp. 728–734).

| **[A9]** Golumbic, M. C., & Shamir, R. (1993). Complexity and
  algorithms for reasoning about time: A graph-theoretic approach.
  *Journal of the ACM, 40*\ (5), 1108–1133.
| 🔒 `ACM (DOI) <https://doi.org/10.1145/174147.169675>`__  ·  📄 `Univ.
  of Haifa
  record <https://cris.haifa.ac.il/en/publications/complexity-and-algorithms-for-reasoning-about-time-a-graph-theore/>`__

| **[A10]** Nebel, B., & Bürckert, H.-J. (1995). Reasoning about
  temporal relations: A maximal tractable subclass of Allen’s interval
  algebra. *Journal of the ACM, 42*\ (1), 43–66.
| 🟢 `earlier DFKI report RR-93-11
  (PDF) <https://dfki.de/fileadmin/user_upload/import/2523_RR-93-11.pdf>`__
   ·  📄 `JACM
  record <https://projects.csail.mit.edu/jacm/References/nebelb1995:43.html>`__
| Note: The free PDF is the 1993 technical report with the same title;
  the journal version is paywalled.

| **[A11]** Jonsson, P., & Bäckström, C. (1998). A unifying approach to
  temporal constraint reasoning. *Artificial Intelligence, 102*\ (1),
  143–155.
| 🔒 `publisher
  (DOI) <https://doi.org/10.1016/S0004-3702%2898%2900031-9>`__

| **[A12]** Krokhin, A., Jeavons, P., & Jonsson, P. (2003). Reasoning
  about temporal relations: The tractable subalgebras of Allen’s
  interval algebra. *Journal of the ACM, 50*\ (5), 591–640.
| 🔒 `ACM (DOI) <https://doi.org/10.1145/876638.876639>`__  ·  🟢
  `Durham accepted
  version <https://durham-repository.worktribe.com/output/1564599>`__
   ·  📄 `Oxford
  record <https://www.cs.ox.ac.uk/publications/publication1679-abstract.html>`__
| Note: The free copy is the author’s accepted version, deposited in
  Durham Research Online.

| **[A13]** Bodirsky, M., & Chen, H. (2007). Qualitative temporal and
  spatial reasoning revisited. In *Computer Science Logic (CSL 2007)*,
  LNCS 4646 (pp. 194–207). Springer.
| 📄 `TU Dresden
  record <https://fis.tu-dresden.de/portal/en/publications/qualitative-temporal-and-spatial-reasoning-revisited-conference-contribution%282b7d2b54-f278-4b35-9904-c626106712be%29.html>`__

| **[A14]** Janhunen, T., & Sioutis, M. (2019). Allen’s interval algebra
  makes the difference. arXiv:1909.01128. Published in *Declarative
  Programming and Knowledge Management (DECLARE 2019)*, LNCS/LNAI 12057
  (pp. 89–98). Springer, 2020.
| 🟢 `arXiv <https://arxiv.org/abs/1909.01128>`__  ·  🟢 `accepted
  manuscript
  (Aalto)† <https://research.aalto.fi/files/43513972/Janhunen_Sioutis_Allen_s_Interval.pdf>`__
   ·  🔒
  `Springer† <https://link.springer.com/chapter/10.1007/978-3-030-46714-2_6>`__
| Note: The arXiv preprint (September 2019) predates the Springer
  version (2020).

| **[A15]** Janhunen, T., & Sioutis, M. (2019). *Allen’s interval
  algebra makes the difference* [Conference talk slides]. Aalto
  University, 10 September 2019.
| *No online copy found.*
| Note: Slides for the paper above. No online copy found.

Metric and Disjunctive Temporal Constraints
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Temporal constraint networks that add metric (quantitative) information
or disjunctions, and the algorithms and planning applications built on
them.

| **[B1]** Dechter, R., Meiri, I., & Pearl, J. (1991). Temporal
  constraint networks. *Artificial Intelligence, 49*\ (1–3), 61–95.
| 🟢 `UCLA reprint
  (PDF) <https://ftp.cs.ucla.edu/pub/stat_ser/r113-L-reprint.pdf>`__

| **[B2]** Schwalb, E., & Dechter, R. (c. 1993). *Processing temporal
  constraint networks*. University of California, Irvine
  (report/preprint).
| 📄 `ResearchGate
  record† <https://www.researchgate.net/publication/2584692_Processing_Temporal_Constraint_Networks>`__
   ·  📄 `UCI report R40 (related journal
  paper) <https://ics.uci.edu/~dechter/publications/r40.html>`__  ·  🔒
  `related: AIJ 93 (1997),
  DOI <https://doi.org/10.1016/S0004-3702%2897%2900009-X>`__
| Note: Date not confirmed. This appears to be a c. 1993 report, and a
  ResearchGate record with this exact title is dated 1997. Closely
  related: Schwalb & Dechter (1997), “Processing disjunctions in
  temporal constraint networks,” *Artificial Intelligence, 93*\ (1–2),
  29–61.

| **[B3]** Tsamardinos, I. (2001). *Constraint-based temporal reasoning
  algorithms with applications to planning* [Doctoral dissertation].
  University of Pittsburgh.
| 📄 `ACM record† <https://dl.acm.org/doi/10.5555/934753>`__  ·  📄
  `ResearchGate
  record† <https://www.researchgate.net/publication/230561978_Constraint-Based_Temporal_Reasoning_Algorithms_with_Applications_to_Planning>`__

| **[B4]** Tsamardinos, I., & Pollack, M. E. (2003). Efficient solution
  techniques for disjunctive temporal reasoning problems. *Artificial
  Intelligence, 151*\ (1–2), 43–89.
| 📄 `metadata
  record <https://datalearner.com:8443/academic/journal-papers/0004-3702/volumes-and-issues/277/paper-detail/1660>`__
| Note: No DOI or free copy found.

Extensions of the Interval Algebra
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Variations on Allen’s algebra: semi-intervals and conceptual
neighborhoods, adding points and branching time, unbounded intervals,
tree-like time, and two-sorted point-interval theories.

| **[C1]** Freksa, C. (1991). Conceptual neighborhood and its role in
  temporal and spatial reasoning. In M. Singh & L. Travé-Massuyès
  (Eds.), *Proceedings of the IMACS Workshop on Decision Support Systems
  and Qualitative Reasoning* (pp. 181–187). North-Holland.
| 🟢 `PDF (SFB/TR 8,
  Bremen) <https://www.sfbtr8.spatial-cognition.de/aigaion/index.php/login/anonymous/cosy_reader/attachments/single/Conceptual%20Neighborhood_h.pdf>`__

| **[C2]** Freksa, C. (1992). Temporal reasoning based on
  semi-intervals. *Artificial Intelligence, 54*, 199–227.
| 🔒 `publisher
  (DOI) <https://doi.org/10.1016/0004-3702%2892%2990090-K>`__  ·  🟢
  `earlier ICSI tech report
  TR-90-016† <https://www1.icsi.berkeley.edu/ftp/pub/techreports/1990/tr-90-016.pdf>`__
| Note: The ICSI report appears to be the 1990 technical-report version
  and may differ from the journal text.

| **[C3]** Reich, A. J. (1994). Intervals, points, and branching time.
  In S. D. Goodwin & H. J. Hamilton (Eds.), *Proceedings of the TIME-94
  International Workshop on Temporal Reasoning* (pp. 121–133).
  University of Regina.
| 📄 `Semantic Scholar
  record <https://www.semanticscholar.org/paper/Intervals%2C-Points%2C-and-Branching-Time-Reich/a12eca974573c812d696f3d0a58bccb171a8c39d>`__
   ·  📄 `ResearchGate
  record† <https://www.researchgate.net/publication/220810644_Intervals_Points_and_Branching_Time>`__
| Note: The paper on which ``qualreas`` is based. Venue and pages as
  cited in the qualreas documentation. A PDF and tables in text format
  are available at the ‘qualreas’ github repo.

| **[C4]** Cukierman, D. R., & Delgrande, J. P. (2004). A theory for
  convex interval relations including unbounded intervals. In
  *Proceedings of FLAIRS 2004*. AAAI Press.
| 🟢 `PDF <https://cdn.aaai.org/FLAIRS/2004/Flairs04-134.pdf>`__

| **[C5]** Durhan, S., & Sciavicco, G. (2015). Generalizing Allen’s
  theory of time to tree-like structures. In *22nd International
  Symposium on Temporal Representation and Reasoning (TIME 2015)*
  (pp. 69–78). IEEE.
| 🔒 `IEEE (DOI) <https://doi.org/10.1109/TIME.2015.17>`__  ·  🟢
  `pre-print (Univ. of
  Ferrara)† <https://iris.unife.it/retrieve/e309ade0-89d6-3969-e053-3a05fe0a2c94/time15-RepTheorems.pdf>`__

| **[C6]** Conradie, W., Durhan, S., & Sciavicco, G. (2020). An
  integrated first-order theory of points and intervals over linear
  orders (Part II). *Logical Methods in Computer Science, 16*\ (2),
  1:1–1:33.
| 🟢 `LMCS (open access) <https://lmcs.episciences.org/6260/pdf>`__  · 
  🟢 `arXiv <https://arxiv.org/abs/1809.04468>`__  ·  🔒
  `DOI <https://doi.org/10.23638/LMCS-16%282:1%292020>`__
| Note: This is Part II of a two-part series. Part I: LMCS 14(2:15),
  2018, `arXiv:1805.08425 <https://arxiv.org/abs/1805.08425>`__.

Relation Algebras and Time Ontologies
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Algebraic and logical foundations: relation algebras of points and
intervals, composition, what a ‘qualitative calculus’ is, catalogs of
temporal theories, and first-order time ontologies.

| **[D1]** Hirsch, R. (1994). From points to intervals. *Journal of
  Applied Non-Classical Logics, 4*\ (1), 7–27.
| 📄 `abstract and citation
  record <https://reliable-computing.org/abstracts/hirsch.html>`__
| Note: No DOI or free copy found.

| **[D2]** Bennett, B. (1994). Some observations and puzzles about
  composing spatial and temporal relations. In *Workshop on Spatial and
  Temporal Reasoning, 11th European Conference on Artificial
  Intelligence (ECAI-94)* (pp. 65–72). Amsterdam.
| 📄 `citation record (A. G. Cohn’s papers
  page) <https://www.ida.liu.se/ext/brs/A/Cohn/webpapers.html>`__
| Note: Citation details come from Cohn’s page. No free PDF found.

| **[D3]** Hayes, P. J. (1996). *A catalog of temporal theories*
  (Technical Report UIUC-BI-AI-96-01). Beckman Institute, University of
  Illinois.
| 🟢 `Part 1
  (PostScript)† <http://www.coginst.uwf.edu/~phayes/TimeCatalog1.ps>`__
   ·  🟢 `Part 2
  (PostScript)† <http://www.coginst.uwf.edu/~phayes/TimeCatalog2.ps>`__
   ·  📄 `Hayes’s papers
  list <https://www.ida.liu.se/ext/brs/A/Hayes/webpapers.html>`__
| Note: Written 1995–96; Hayes’s own list gives 1995.

| **[D4]** Hirsch, R. (1996). Relation algebras of intervals.
  *Artificial Intelligence, 83*\ (2), 267–295.
| 🔒
  `ScienceDirect† <https://www.sciencedirect.com/science/article/pii/0004370295000429>`__
   ·  📄 `dblp (author
  page) <https://dblp1.uni-trier.de/pid/04/4775.html>`__

| **[D5]** Hobbs, J. R., & Pan, F. (2004). An ontology of time for the
  Semantic Web. *ACM Transactions on Asian Language Information
  Processing, 3*\ (1), 66–85.
| 🔒 `ACM (DOI) <https://doi.org/10.1145/1017068.1017073>`__  ·  🟢
  `author’s PDF
  (USC/ISI)† <https://www.isi.edu/people-hobbs/wp-content/uploads/sites/58/2023/11/hobbs-pan-TALIP.pdf>`__

| **[D6]** Ligozat, G., & Renz, J. (2004). What is a qualitative
  calculus? A general framework. In *PRICAI 2004: Trends in Artificial
  Intelligence*, LNCS 3157 (pp. 53–64). Springer.
| 🔒
  `Springer <https://link.springer.com/doi/10.1007/978-3-540-28633-2_8>`__
   ·  🟢 `HAL
  deposit† <https://hal.archives-ouvertes.fr/hal-01487502>`__  ·  🟢
  `ANU
  repository† <https://openresearch-repository.anu.edu.au/items/a02965b1-a8d9-4c16-bec8-4534f3768a1e/full>`__
| Note: Not to be confused with the later journal paper “So, what
  exactly is a qualitative calculus?” is a different, later work.

| **[D7]** Grüninger, M. (2011). Verification of the OWL-Time ontology.
  In *The Semantic Web – ISWC 2011*, LNCS 7031 (pp. 225–240). Springer.
| 🔒 `Springer (DOI) <https://doi.org/10.1007/978-3-642-25073-6_15>`__
   ·  📄 `BibBase
  record <https://bibbase.org/network/publication/grninger-verificationoftheowltimeontology-2011>`__

| **[D8]** Grüninger, M., & Li, Z. (2017). The time ontology of Allen’s
  interval algebra. In *24th International Symposium on Temporal
  Representation and Reasoning (TIME 2017)*, LIPIcs 90 (16:1–16:16).
  Schloss Dagstuhl.
| 🟢 `Dagstuhl (open
  access) <https://drops.dagstuhl.de/entities/document/10.4230/LIPIcs.TIME.2017.16>`__
   ·  🔒 `DOI <https://doi.org/10.4230/LIPIcs.TIME.2017.16>`__

Qualitative Spatial Reasoning
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Spatial counterparts of Allen’s algebra: the Region Connection Calculus
and its composition tables, cardinal directions, ternary point calculi
and 3D / multidimensional extensions.

| **[E1]** Frank, A. U. (1991). Qualitative spatial reasoning about
  cardinal directions. In *Proceedings of ACSM-ASPRS Auto-Carto 10*
  (pp. 148–167). Baltimore.
| 🟢 `PDF (CartoGIS
  archive) <https://cartogis.org/docs/proceedings/archive/auto-carto-10/pdf/qualitative-spatial-reasoning-about-cardinal-directions.pdf>`__
| Note: Presented in 1991; the draft is dated 1990.

| **[E2]** Randell, D. A., Cui, Z., & Cohn, A. G. (1992). A spatial
  logic based on regions and connection. In *Proceedings of the 3rd
  International Conference on Principles of Knowledge Representation and
  Reasoning (KR’92)*. Morgan Kaufmann.
| 📄 `citation record (A. G. Cohn’s papers
  page) <https://www.ida.liu.se/ext/brs/A/Cohn/webpapers.html>`__
| Note: The foundational RCC paper. No free copy found; Cohn’s page
  lists only a Leeds FTP file.

| **[E3]** Li, S., & Ying, M. (2003). Region connection calculus: Its
  models and composition table. *Artificial Intelligence, 145*\ (1–2),
  121–146.
| 🔒 `publisher
  (DOI) <https://doi.org/10.1016/S0004-3702%2802%2900372-7>`__  ·  📄
  `UTS repository record (closed
  access) <https://opus.lib.uts.edu.au/handle/10453/9059>`__
| Note: Published online in 2002; the issue is dated 2003.

| **[E4]** Scivos, A., & Nebel, B. (2004). The finest of its class: The
  natural, point-based ternary calculus LR for qualitative spatial
  reasoning. In *Spatial Cognition IV: Reasoning, Action, Interaction*,
  LNAI 3343 (pp. 283–303). Springer.
| 🔒 `Springer
  volume <https://link.springer.com/book/10.1007/b106616>`__  ·  📄
  `ResearchGate
  record† <https://www.researchgate.net/publication/221104118>`__
| Note: Presented in 2004; the proceedings volume is dated 2005 by the
  publisher.

| **[E5]** Sabharwal, C. L., Leopold, J. L., & Eloe, N. (2011). A more
  expressive 3D region connection calculus. In *Proceedings of the 17th
  International Conference on Distributed Multimedia Systems (DMS 2011)*
  (pp. 307–311). Knowledge Systems Institute Graduate School.
| 📄 `Missouri S&T
  record <https://mst.elsevierpure.com/en/publications/a-more-expressive-3d-region-connection-calculus/>`__
   ·  📄 `ResearchGate
  record† <https://www.researchgate.net/publication/267705841>`__

| **[E6]** Sabharwal, C. L., & Leopold, J. L. (2012). An efficient
  algorithm for generating composition tables for qualitative spatial
  relations. In *Proceedings of the 25th International Conference on
  Computer Applications in Industry and Engineering (CAINE 2012)*
  (pp. 29–34). New Orleans.
| 📄 `Missouri S&T
  record <https://scholarsmine.mst.edu/comsci_facwork/1618>`__

| **[E7]** Ghosh, M. (2013). *Region connection calculus: Composition
  tables and constraint satisfaction problems* [Master’s thesis]. Brock
  University.
| 📄 `Brock repository
  record <https://brocku.scholaris.ca/items/e10f26de-b853-40ad-b5ac-386f791d85fb>`__

| **[E8]** Schockaert, S., & Li, S. (2013). Combining RCC5 relations
  with betweenness information. In *Proceedings of the Twenty-Third
  International Joint Conference on Artificial Intelligence (IJCAI
  2013)*. AAAI Press.
| 🟢 `PDF <https://ijcai.org/proceedings/2013/0164.pdf>`__  ·  📄 `IJCAI
  abstract page <https://ijcai.org/Abstract/13/164>`__

| **[E9]** Izadi, A., Stock, K. M., & Guesgen, H. W. (c. 2017).
  *Multidimensional region connection calculus*. Massey University
  (workshop paper).
| 🟢 `PDF (QR 2017 workshop
  site) <https://www.qrg.northwestern.edu/qr2017/papers/QR2017_paper_8.pdf>`__
| Note: Venue and year not confirmed. The PDF is hosted on the site of
  the QR 2017 qualitative-reasoning workshop and cites 2017 work,
  although it carries a 2015 AAAI copyright line.

Software and Implementations
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Reasoners, toolkits and implementations of interval and qualitative
calculi: Prolog, TIMELOGIC, SparQ, GQR, Semantic Web rules and Linked
Data link generation.

| **[F1]** Koomen, J. A. G. M. (1989). *The TIMELOGIC temporal reasoning
  system* (Technical Report 231, revised for version 3.x). Department of
  Computer Science, University of Rochester.
| 🟢 `Rochester repository
  (PDF)† <https://urresearch.rochester.edu/fileDownloadForInstitutionalItem.action?itemId=5605&itemFileId=8649>`__

| **[F2]** Hrycej, T. (1993). A temporal extension of Prolog. *Journal
  of Logic Programming, 15*\ (1–2), 113–145.
| 📄 `dblp record <https://vldb.org/dblp/db/journals/jlp/jlp15.html>`__
| Note: No DOI or free copy found.

| **[F3]** Alspaugh, T. A. (2005). *Software support for calculations in
  Allen’s interval algebra* (Technical Report UCI-ISR-05-2). Institute
  for Software Research, University of California, Irvine.
| 📄 `UCI ISR report page <https://isr.uci.edu/node/803.html>`__  ·  📄
  `author’s Allen’s-algebra software
  page <https://ics.uci.edu/~alspaugh/cls/shr/allen.html>`__

| **[F4]** Dylla, F., Frommberger, L., Wallgrün, J. O., & Wolter, D.
  (2006). SparQ: A toolbox for qualitative spatial representation and
  reasoning. In *Workshop on Qualitative Constraint Calculi: Application
  and Integration, KI 2006*. Bremen.
| 📄 `SFB/TR 8
  record <https://cindy.informatik.uni-bremen.de/www3/www.sfbtr8.spatial-cognition.de/aigaion/index.php/publications/show/152.html>`__
   ·  📄 `SparQ project
  page <https://www.uni-bamberg.de/sme/research/sparq>`__

| **[F5]** Gantner, Z., Westphal, M., & Wölfl, S. (2008). GQR – A fast
  reasoner for binary qualitative constraint calculi. AAAI Press (AAAI
  2008 workshop paper).
| 🟢 `PDF (Univ. of
  Freiburg) <https://gki.informatik.uni-freiburg.de/papers/gantner-etal-aaai-08.pdf>`__
| Note: The exact AAAI workshop name was not confirmed.

| **[F6]** Wolter, D. (2009). SparQ – A spatial reasoning toolbox. In
  *Benchmarking of Qualitative Spatial and Temporal Reasoning Systems:
  Papers from the 2009 AAAI Spring Symposium* (AAAI Technical Report
  SS-09-02). AAAI Press.
| 📄 `AAAI proceedings page <https://aaai.org/?p=65136>`__

| **[F7]** Endelin, R., Aloulou, H., De Roo, J., Renouard, S.,
  Tiberghien, T., & Mokhtari, M. (2013). Implementation of Allen’s
  interval logic with the Semantic Web. In *Proceedings of the 5th
  International Conference on Management of Emergent Digital EcoSystems
  (MEDES ’13)* (pp. 252–253). ACM.
| 🔒 `ACM (DOI) <https://doi.org/10.1145/2536146.2536181>`__  ·  🟢 `HAL
  deposit† <https://hal.science/hal-01098461>`__

| **[F8]** Georgala, K., Sherif, M. A., & Ngonga Ngomo, A.-C. (2016). An
  efficient approach for the generation of Allen relations. In *ECAI
  2016*, Frontiers in Artificial Intelligence and Applications 285
  (pp. 948–956). IOS Press.
| 🔒 `IOS Press (DOI) <https://doi.org/10.3233/978-1-61499-672-9-948>`__
   ·  📄 `Paderborn
  record <https://ris.uni-paderborn.de/record/26466>`__

Applications and Cognitive Studies
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Uses of Allen-style relations outside core reasoning research: cognitive
experiments, Bayesian networks, interval data mining, process modeling,
and course notes.

| **[G1]** Knauff, M. (1999). The cognitive adequacy of Allen’s interval
  calculus for qualitative spatial representation and reasoning.
  *Spatial Cognition and Computation, 1*, 261–290.
| 📄 `Max Planck record (probable
  match) <https://pure.mpg.de/pubman/item/item_1793800_2>`__
| Note: No free copy found.

| **[G2]** Tawfik, A. Y., & Neufeld, E. (2000). Temporal reasoning and
  Bayesian networks. *Computational Intelligence, 16*\ (3).
| 🔒 `publisher (DOI) <https://doi.org/10.1111/0824-7935.00116>`__  · 
  📄 `ResearchGate
  record† <https://www.researchgate.net/publication/215444297>`__
| Note: Page range not confirmed.

| **[G3]** Mörchen, F. (2006). A better tool than Allen’s relations for
  expressing temporal knowledge in interval data. In *Workshop on
  Temporal Data Mining, 12th ACM SIGKDD International Conference on
  Knowledge Discovery and Data Mining* (pp. 25–34).
| *No online copy found.*
| Note: Venue taken from a reference in Mörchen’s own survey. No online
  copy found.

| **[G4]** Gagné, D., & Trudel, A. (2007). A formal temporal semantics
  for Microsoft Project based on Allen’s interval algebra. (A paper with
  this title also appears in *Business Process, Services Computing and
  Intelligent Service Management*, LNI P-147, Gesellschaft für
  Informatik, 2009, pp. 32–45.)
| 🟢 `GI Digital Library (open
  repository) <https://dl.gi.de/items/2b7e9c8d-476f-4c75-aa1c-3351315c23ac/full>`__
   ·  📄 `AAAI abstract page <https://aaai.org/?p=83475>`__
| Note: The 2007 venue was not confirmed; the only fully documented
  record is the 2009 LNI one.

| **[G5]** Crowley, J. L. (2013). *Temporal reasoning – Allen’s temporal
  logic* [Lecture notes, Lesson 9, Intelligent Systems: Reasoning and
  Recognition, ENSIMAG 2 / MoSIG M1, 15 March 2013].
| 📄 `author’s homepage† <http://crowley-coutaz.fr/jlc/jlc.html>`__
| Note: Course notes. The lecture PDF itself was not located online.

Temporal Reasoning in Natural Language Processing
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Extracting and reasoning about event/time relations in text, including
timeline extraction and the learning of temporal relations.

| **[H1]** Moldovan, D., Clark, C., & Harabagiu, S. (2005). Temporal
  context representation and reasoning. In *Proceedings of the 19th
  International Joint Conference on Artificial Intelligence (IJCAI-05)*
  (pp. 1099–1104).
| 🟢 `PDF† <https://ijcai.org/Proceedings/05/Papers/1538.pdf>`__  ·  📄
  `ML Anthology
  record <https://mlanthology.org/ijcai/2005/moldovan2005ijcai-temporal>`__

| **[H2]** Bethard, S., Martin, J. H., & Klingenstein, S. (2007).
  Timelines from text: Identification of syntactic temporal relations.
  In *International Conference on Semantic Computing (ICSC 2007)*
  (pp. 11–18). IEEE.
| 🔒 `IEEE (DOI) <https://doi.org/10.1109/ICSC.2007.77>`__  ·  📄 `CU
  Boulder record <https://vivo.colorado.edu/display/pubid_72362>`__

| **[H3]** Kolomiyets, O., Bethard, S., & Moens, M.-F. (2012).
  Extracting narrative timelines as temporal dependency structures. In
  *Proceedings of the 50th Annual Meeting of the Association for
  Computational Linguistics (ACL 2012)* (pp. 88–97).
| 🟢 `PDF (ACL Anthology)† <https://aclanthology.org/P12-1010.pdf>`__
   ·  📄 `ACL Anthology page <https://aclanthology.org/P12-1010/>`__

| **[H4]** Derczynski, L. (2016). Representation and learning of
  temporal relations. In *Proceedings of COLING 2016, the 26th
  International Conference on Computational Linguistics: Technical
  Papers* (pp. 1937–1948).
| 🟢 `PDF (ACL Anthology)† <https://aclanthology.org/C16-1182.pdf>`__
   ·  📄 `ACL Anthology page <https://aclanthology.org/C16-1182/>`__

Surveys and Overviews
~~~~~~~~~~~~~~~~~~~~~

Broad overviews, which cut across the topics above: general temporal
reasoning in AI, constraint-based temporal reasoning, qualitative
spatial reasoning, relation algebras, and NLP.

| **[I1]** Vila, L. (1994). A survey on temporal reasoning in artificial
  intelligence. *AI Communications, 7*\ (1), 4–28.
| 🟢 `author’s copy
  (PostScript)† <http://www.lsi.upc.es/~vila/vila/trs/trs.ps.gz>`__  · 
  🔒 `IOS
  Press <https://content.iospress.com/articles/ai-communications/aic7-1-02>`__
   ·  📄 `author’s publications
  page <https://www.cs.upc.edu/~vila/vila/papers.html>`__

| **[I2]** Gennari, R. (1998). Temporal reasoning and constraint
  programming: A survey. *CWI Quarterly, 11*\ (2–3), 163–214.
| 🟢 `PDF (CWI repository) <https://ir.cwi.nl/pub/18330/18330B.pdf>`__
   ·  📄 `CWI repository record <https://ir.cwi.nl/pub/18330>`__

| **[I3]** Cohn, A. G., & Hazarika, S. M. (2001). Qualitative spatial
  representation and reasoning: An overview. *Fundamenta Informaticae,
  46*\ (1–2), 1–29.
| 🔒 `IOS
  Press <https://content.iospress.com/articles/fundamenta-informaticae/fi46-1-2-02>`__
   ·  📄 `ACM record <https://dl.acm.org/doi/10.5555/1219982.1219984>`__

| **[I4]** Düntsch, I. (2005). Relation algebras and their application
  in temporal and spatial reasoning. *Artificial Intelligence Review,
  23*, 315–357.
| 📄 `Brock tech report CS-05-01
  record <https://www2.cosc.brocku.ca/archive/node/144>`__  ·  📄
  `author’s publication
  list <https://cosc.brocku.ca/~duentsch/papers/idpub_bib.html>`__
| Note: A preprint appeared as Brock University Technical Report
  CS-05-01 (February 2005).

| **[I5]** Renz, J., & Nebel, B. (2007). Qualitative spatial reasoning
  using constraint calculi. In M. Aiello, I. Pratt-Hartmann, & J. van
  Benthem (Eds.), *Handbook of Spatial Logics* (pp. 161–215). Springer.
| 🔒 `Springer book
  page <https://link.springer.com/book/10.1007/978-1-4020-5587-4>`__  · 
  📄 `ANU
  record† <https://researchportalplus.anu.edu.au/en/publications/qualitative-spatial-reasoning-using-constraint-calculi/>`__

| **[I6]** Planken, L. (2007). *Temporal reasoning problems and
  algorithms for solving them* [Literature survey, 2 November 2007].
  Delft University of Technology.
| 🟢 `PDF (hosted at Univ. of
  Nebraska–Lincoln) <http://cse.unl.edu/~choueiry/Documents/Planken-TCSP-literature-survey.pdf>`__
   ·  📄 `TU Delft repository
  record† <https://repository.tudelft.nl/islandora/object/uuid:3bd04df1-6392-4837-8d19-c4b5d4a3a84d>`__

| **[I7]** Sanampudi, S. K., & Kumari, G. V. (2010). Temporal reasoning
  in natural language processing: A survey. *International Journal of
  Computer Applications, 1*\ (4), 53–57.
| 🟢 `PDF <https://www.ijcaonline.org/journal/number4/pxc387209.pdf>`__
   ·  🔒 `journal
  page <https://ijcaonline.org/archives/volume1/number4/100-209/>`__  · 
  🔒 `DOI <https://doi.org/10.5120/100-209>`__

4. All Works in Chronological Order
-----------------------------------

The ID in the last column points to the full entry in Section 3.

+-----------------+-----------------+------------------+-----------------+
| Year            | Authors         | Title            | ID              |
+=================+=================+==================+=================+
| 1982            | Vilain, M. B.   | A system for     | A1              |
|                 |                 | reasoning about  |                 |
|                 |                 | time             |                 |
+-----------------+-----------------+------------------+-----------------+
| 1983            | Allen, J. F.    | Maintaining      | A2              |
|                 |                 | knowledge about  |                 |
|                 |                 | temporal         |                 |
|                 |                 | intervals        |                 |
+-----------------+-----------------+------------------+-----------------+
| 1986            | Vilain, M., &   | Constraint       | A3              |
|                 | Kautz, H.       | propagation      |                 |
|                 |                 | algorithms for   |                 |
|                 |                 | temporal         |                 |
|                 |                 | reasoning        |                 |
+-----------------+-----------------+------------------+-----------------+
| 1987            | Tsang, E. P. K. | The consistent   | A4              |
|                 |                 | labeling problem |                 |
|                 |                 | in temporal      |                 |
|                 |                 | reasoning        |                 |
+-----------------+-----------------+------------------+-----------------+
| 1989            | van Beek, P.    | Approximation    | A5              |
|                 |                 | algorithms for   |                 |
|                 |                 | temporal         |                 |
|                 |                 | reasoning        |                 |
+-----------------+-----------------+------------------+-----------------+
| 1989            | Koomen, J. A.   | The TIMELOGIC    | F1              |
|                 | G. M.           | temporal         |                 |
|                 |                 | reasoning system |                 |
+-----------------+-----------------+------------------+-----------------+
| 1990            | Vilain, M.,     | Constraint       | A6              |
|                 | Kautz, H., &    | propagation      |                 |
|                 | van Beek, P.    | algorithms for   |                 |
|                 |                 | temporal         |                 |
|                 |                 | reasoning: A     |                 |
|                 |                 | revised report   |                 |
+-----------------+-----------------+------------------+-----------------+
| 1990            | van Beek, P., & | Exact and        | A7              |
|                 | Cohen, R.       | approximate      |                 |
|                 |                 | reasoning about  |                 |
|                 |                 | temporal         |                 |
|                 |                 | relations        |                 |
+-----------------+-----------------+------------------+-----------------+
| 1991            | Dechter, R.,    | Temporal         | B1              |
|                 | Meiri, I., &    | constraint       |                 |
|                 | Pearl, J.       | networks         |                 |
+-----------------+-----------------+------------------+-----------------+
| 1991            | Freksa, C.      | Conceptual       | C1              |
|                 |                 | neighborhood and |                 |
|                 |                 | its role in      |                 |
|                 |                 | temporal and     |                 |
|                 |                 | spatial          |                 |
|                 |                 | reasoning        |                 |
+-----------------+-----------------+------------------+-----------------+
| 1991            | Frank, A. U.    | Qualitative      | E1              |
|                 |                 | spatial          |                 |
|                 |                 | reasoning about  |                 |
|                 |                 | cardinal         |                 |
|                 |                 | directions       |                 |
+-----------------+-----------------+------------------+-----------------+
| 1992            | van Beek, P.    | Reasoning about  | A8              |
|                 |                 | qualitative      |                 |
|                 |                 | temporal         |                 |
|                 |                 | information      |                 |
+-----------------+-----------------+------------------+-----------------+
| 1992            | Freksa, C.      | Temporal         | C2              |
|                 |                 | reasoning based  |                 |
|                 |                 | on               |                 |
|                 |                 | semi-intervals   |                 |
+-----------------+-----------------+------------------+-----------------+
| 1992            | Randell, D. A., | A spatial logic  | E2              |
|                 | Cui, Z., &      | based on regions |                 |
|                 | Cohn, A. G.     | and connection   |                 |
+-----------------+-----------------+------------------+-----------------+
| 1993            | Golumbic, M.    | Complexity and   | A9              |
|                 | C., & Shamir,   | algorithms for   |                 |
|                 | R.              | reasoning about  |                 |
|                 |                 | time: A          |                 |
|                 |                 | graph-theoretic  |                 |
|                 |                 | approach         |                 |
+-----------------+-----------------+------------------+-----------------+
| 1993            | Schwalb, E., &  | Processing       | B2              |
|                 | Dechter, R.     | temporal         |                 |
|                 |                 | constraint       |                 |
|                 |                 | networks         |                 |
+-----------------+-----------------+------------------+-----------------+
| 1993            | Hrycej, T.      | A temporal       | F2              |
|                 |                 | extension of     |                 |
|                 |                 | Prolog           |                 |
+-----------------+-----------------+------------------+-----------------+
| 1994            | Reich, A. J.    | Intervals,       | C3              |
|                 |                 | points, and      |                 |
|                 |                 | branching time   |                 |
+-----------------+-----------------+------------------+-----------------+
| 1994            | Hirsch, R.      | From points to   | D1              |
|                 |                 | intervals        |                 |
+-----------------+-----------------+------------------+-----------------+
| 1994            | Vila, L.        | A survey on      | I1              |
|                 |                 | temporal         |                 |
|                 |                 | reasoning in     |                 |
|                 |                 | artificial       |                 |
|                 |                 | intelligence     |                 |
+-----------------+-----------------+------------------+-----------------+
| 1994            | Bennett, B.     | Some             | D2              |
|                 |                 | observations and |                 |
|                 |                 | puzzles about    |                 |
|                 |                 | composing        |                 |
|                 |                 | spatial and      |                 |
|                 |                 | temporal         |                 |
|                 |                 | relations        |                 |
+-----------------+-----------------+------------------+-----------------+
| 1995            | Nebel, B., &    | Reasoning about  | A10             |
|                 | Bürckert, H.-J. | temporal         |                 |
|                 |                 | relations: A     |                 |
|                 |                 | maximal          |                 |
|                 |                 | tractable        |                 |
|                 |                 | subclass of      |                 |
|                 |                 | Allen’s interval |                 |
|                 |                 | algebra          |                 |
+-----------------+-----------------+------------------+-----------------+
| 1996            | Hayes, P. J.    | A catalog of     | D3              |
|                 |                 | temporal         |                 |
|                 |                 | theories         |                 |
+-----------------+-----------------+------------------+-----------------+
| 1996            | Hirsch, R.      | Relation         | D4              |
|                 |                 | algebras of      |                 |
|                 |                 | intervals        |                 |
+-----------------+-----------------+------------------+-----------------+
| 1998            | Jonsson, P., &  | A unifying       | A11             |
|                 | Bäckström, C.   | approach to      |                 |
|                 |                 | temporal         |                 |
|                 |                 | constraint       |                 |
|                 |                 | reasoning        |                 |
+-----------------+-----------------+------------------+-----------------+
| 1998            | Gennari, R.     | Temporal         | I2              |
|                 |                 | reasoning and    |                 |
|                 |                 | constraint       |                 |
|                 |                 | programming: A   |                 |
|                 |                 | survey           |                 |
+-----------------+-----------------+------------------+-----------------+
| 1999            | Knauff, M.      | The cognitive    | G1              |
|                 |                 | adequacy of      |                 |
|                 |                 | Allen’s interval |                 |
|                 |                 | calculus for     |                 |
|                 |                 | qualitative      |                 |
|                 |                 | spatial          |                 |
|                 |                 | representation   |                 |
|                 |                 | and reasoning    |                 |
+-----------------+-----------------+------------------+-----------------+
| 2000            | Tawfik, A. Y.,  | Temporal         | G2              |
|                 | & Neufeld, E.   | reasoning and    |                 |
|                 |                 | Bayesian         |                 |
|                 |                 | networks         |                 |
+-----------------+-----------------+------------------+-----------------+
| 2001            | Tsamardinos, I. | Constraint-based | B3              |
|                 |                 | temporal         |                 |
|                 |                 | reasoning        |                 |
|                 |                 | algorithms with  |                 |
|                 |                 | applications to  |                 |
|                 |                 | planning         |                 |
+-----------------+-----------------+------------------+-----------------+
| 2001            | Cohn, A. G., &  | Qualitative      | I3              |
|                 | Hazarika, S. M. | spatial          |                 |
|                 |                 | representation   |                 |
|                 |                 | and reasoning:   |                 |
|                 |                 | An overview      |                 |
+-----------------+-----------------+------------------+-----------------+
| 2003            | Krokhin, A.,    | Reasoning about  | A12             |
|                 | Jeavons, P., &  | temporal         |                 |
|                 | Jonsson, P.     | relations: The   |                 |
|                 |                 | tractable        |                 |
|                 |                 | subalgebras of   |                 |
|                 |                 | Allen’s interval |                 |
|                 |                 | algebra          |                 |
+-----------------+-----------------+------------------+-----------------+
| 2003            | Tsamardinos,    | Efficient        | B4              |
|                 | I., & Pollack,  | solution         |                 |
|                 | M. E.           | techniques for   |                 |
|                 |                 | disjunctive      |                 |
|                 |                 | temporal         |                 |
|                 |                 | reasoning        |                 |
|                 |                 | problems         |                 |
+-----------------+-----------------+------------------+-----------------+
| 2003            | Li, S., & Ying, | Region           | E3              |
|                 | M.              | connection       |                 |
|                 |                 | calculus: Its    |                 |
|                 |                 | models and       |                 |
|                 |                 | composition      |                 |
|                 |                 | table            |                 |
+-----------------+-----------------+------------------+-----------------+
| 2004            | Cukierman, D.   | A theory for     | C4              |
|                 | R., &           | convex interval  |                 |
|                 | Delgrande, J.   | relations        |                 |
|                 | P.              | including        |                 |
|                 |                 | unbounded        |                 |
|                 |                 | intervals        |                 |
+-----------------+-----------------+------------------+-----------------+
| 2004            | Hobbs, J. R., & | An ontology of   | D5              |
|                 | Pan, F.         | time for the     |                 |
|                 |                 | Semantic Web     |                 |
+-----------------+-----------------+------------------+-----------------+
| 2004            | Scivos, A., &   | The finest of    | E4              |
|                 | Nebel, B.       | its class: The   |                 |
|                 |                 | natural,         |                 |
|                 |                 | point-based      |                 |
|                 |                 | ternary calculus |                 |
|                 |                 | LR for           |                 |
|                 |                 | qualitative      |                 |
|                 |                 | spatial          |                 |
|                 |                 | reasoning        |                 |
+-----------------+-----------------+------------------+-----------------+
| 2004            | Ligozat, G., &  | What is a        | D6              |
|                 | Renz, J.        | qualitative      |                 |
|                 |                 | calculus? A      |                 |
|                 |                 | general          |                 |
|                 |                 | framework        |                 |
+-----------------+-----------------+------------------+-----------------+
| 2005            | Alspaugh, T. A. | Software support | F3              |
|                 |                 | for calculations |                 |
|                 |                 | in Allen’s       |                 |
|                 |                 | interval algebra |                 |
+-----------------+-----------------+------------------+-----------------+
| 2005            | Düntsch, I.     | Relation         | I4              |
|                 |                 | algebras and     |                 |
|                 |                 | their            |                 |
|                 |                 | application in   |                 |
|                 |                 | temporal and     |                 |
|                 |                 | spatial          |                 |
|                 |                 | reasoning        |                 |
+-----------------+-----------------+------------------+-----------------+
| 2005            | Moldovan, D.,   | Temporal context | H1              |
|                 | Clark, C., &    | representation   |                 |
|                 | Harabagiu, S.   | and reasoning    |                 |
+-----------------+-----------------+------------------+-----------------+
| 2006            | Dylla, F.,      | SparQ: A toolbox | F4              |
|                 | Frommberger,    | for qualitative  |                 |
|                 | L., Wallgrün,   | spatial          |                 |
|                 | J. O., &        | representation   |                 |
|                 | Wolter, D.      | and reasoning    |                 |
+-----------------+-----------------+------------------+-----------------+
| 2006            | Mörchen, F.     | A better tool    | G3              |
|                 |                 | than Allen’s     |                 |
|                 |                 | relations for    |                 |
|                 |                 | expressing       |                 |
|                 |                 | temporal         |                 |
|                 |                 | knowledge in     |                 |
|                 |                 | interval data    |                 |
+-----------------+-----------------+------------------+-----------------+
| 2007            | Bodirsky, M., & | Qualitative      | A13             |
|                 | Chen, H.        | temporal and     |                 |
|                 |                 | spatial          |                 |
|                 |                 | reasoning        |                 |
|                 |                 | revisited        |                 |
+-----------------+-----------------+------------------+-----------------+
| 2007            | Gagné, D., &    | A formal         | G4              |
|                 | Trudel, A.      | temporal         |                 |
|                 |                 | semantics for    |                 |
|                 |                 | Microsoft        |                 |
|                 |                 | Project based on |                 |
|                 |                 | Allen’s interval |                 |
|                 |                 | algebra          |                 |
+-----------------+-----------------+------------------+-----------------+
| 2007            | Renz, J., &     | Qualitative      | I5              |
|                 | Nebel, B.       | spatial          |                 |
|                 |                 | reasoning using  |                 |
|                 |                 | constraint       |                 |
|                 |                 | calculi          |                 |
+-----------------+-----------------+------------------+-----------------+
| 2007            | Bethard, S.,    | Timelines from   | H2              |
|                 | Martin, J. H.,  | text:            |                 |
|                 | & Klingenstein, | Identification   |                 |
|                 | S.              | of syntactic     |                 |
|                 |                 | temporal         |                 |
|                 |                 | relations        |                 |
+-----------------+-----------------+------------------+-----------------+
| 2007            | Planken, L.     | Temporal         | I6              |
|                 |                 | reasoning        |                 |
|                 |                 | problems and     |                 |
|                 |                 | algorithms for   |                 |
|                 |                 | solving them     |                 |
+-----------------+-----------------+------------------+-----------------+
| 2008            | Gantner, Z.,    | GQR – A fast     | F5              |
|                 | Westphal, M., & | reasoner for     |                 |
|                 | Wölfl, S.       | binary           |                 |
|                 |                 | qualitative      |                 |
|                 |                 | constraint       |                 |
|                 |                 | calculi          |                 |
+-----------------+-----------------+------------------+-----------------+
| 2009            | Wolter, D.      | SparQ – A        | F6              |
|                 |                 | spatial          |                 |
|                 |                 | reasoning        |                 |
|                 |                 | toolbox          |                 |
+-----------------+-----------------+------------------+-----------------+
| 2010            | Sanampudi, S.   | Temporal         | I7              |
|                 | K., & Kumari,   | reasoning in     |                 |
|                 | G. V.           | natural language |                 |
|                 |                 | processing: A    |                 |
|                 |                 | survey           |                 |
+-----------------+-----------------+------------------+-----------------+
| 2011            | Grüninger, M.   | Verification of  | D7              |
|                 |                 | the OWL-Time     |                 |
|                 |                 | ontology         |                 |
+-----------------+-----------------+------------------+-----------------+
| 2011            | Sabharwal, C.   | A more           | E5              |
|                 | L., Leopold, J. | expressive 3D    |                 |
|                 | L., & Eloe, N.  | region           |                 |
|                 |                 | connection       |                 |
|                 |                 | calculus         |                 |
+-----------------+-----------------+------------------+-----------------+
| 2012            | Sabharwal, C.   | An efficient     | E6              |
|                 | L., & Leopold,  | algorithm for    |                 |
|                 | J. L.           | generating       |                 |
|                 |                 | composition      |                 |
|                 |                 | tables for       |                 |
|                 |                 | qualitative      |                 |
|                 |                 | spatial          |                 |
|                 |                 | relations        |                 |
+-----------------+-----------------+------------------+-----------------+
| 2012            | Kolomiyets, O., | Extracting       | H3              |
|                 | Bethard, S., &  | narrative        |                 |
|                 | Moens, M.-F.    | timelines as     |                 |
|                 |                 | temporal         |                 |
|                 |                 | dependency       |                 |
|                 |                 | structures       |                 |
+-----------------+-----------------+------------------+-----------------+
| 2013            | Crowley, J. L.  | Temporal         | G5              |
|                 |                 | reasoning –      |                 |
|                 |                 | Allen’s temporal |                 |
|                 |                 | logic            |                 |
+-----------------+-----------------+------------------+-----------------+
| 2013            | Ghosh, M.       | Region           | E7              |
|                 |                 | connection       |                 |
|                 |                 | calculus:        |                 |
|                 |                 | Composition      |                 |
|                 |                 | tables and       |                 |
|                 |                 | constraint       |                 |
|                 |                 | satisfaction     |                 |
|                 |                 | problems         |                 |
+-----------------+-----------------+------------------+-----------------+
| 2013            | Schockaert, S., | Combining RCC5   | E8              |
|                 | & Li, S.        | relations with   |                 |
|                 |                 | betweenness      |                 |
|                 |                 | information      |                 |
+-----------------+-----------------+------------------+-----------------+
| 2013            | Endelin, R.,    | Implementation   | F7              |
|                 | Aloulou, H., De | of Allen’s       |                 |
|                 | Roo, J.,        | interval logic   |                 |
|                 | Renouard, S.,   | with the         |                 |
|                 | Tiberghien, T., | Semantic Web     |                 |
|                 | & Mokhtari, M.  |                  |                 |
+-----------------+-----------------+------------------+-----------------+
| 2015            | Durhan, S., &   | Generalizing     | C5              |
|                 | Sciavicco, G.   | Allen’s theory   |                 |
|                 |                 | of time to       |                 |
|                 |                 | tree-like        |                 |
|                 |                 | structures       |                 |
+-----------------+-----------------+------------------+-----------------+
| 2016            | Georgala, K.,   | An efficient     | F8              |
|                 | Sherif, M. A.,  | approach for the |                 |
|                 | & Ngonga Ngomo, | generation of    |                 |
|                 | A.-C.           | Allen relations  |                 |
+-----------------+-----------------+------------------+-----------------+
| 2016            | Derczynski, L.  | Representation   | H4              |
|                 |                 | and learning of  |                 |
|                 |                 | temporal         |                 |
|                 |                 | relations        |                 |
+-----------------+-----------------+------------------+-----------------+
| 2017            | Grüninger, M.,  | The time         | D8              |
|                 | & Li, Z.        | ontology of      |                 |
|                 |                 | Allen’s interval |                 |
|                 |                 | algebra          |                 |
+-----------------+-----------------+------------------+-----------------+
| 2017            | Izadi, A.,      | Multidimensional | E9              |
|                 | Stock, K. M., & | region           |                 |
|                 | Guesgen, H. W.  | connection       |                 |
|                 |                 | calculus         |                 |
+-----------------+-----------------+------------------+-----------------+
| 2019            | Janhunen, T., & | Allen’s interval | A14             |
|                 | Sioutis, M.     | algebra makes    |                 |
|                 |                 | the difference   |                 |
+-----------------+-----------------+------------------+-----------------+
| 2019            | Janhunen, T., & | Allen’s interval | A15             |
|                 | Sioutis, M.     | algebra makes    |                 |
|                 |                 | the difference   |                 |
+-----------------+-----------------+------------------+-----------------+
| 2020            | Conradie, W.,   | An integrated    | C6              |
|                 | Durhan, S., &   | first-order      |                 |
|                 | Sciavicco, G.   | theory of points |                 |
|                 |                 | and intervals    |                 |
|                 |                 | over linear      |                 |
|                 |                 | orders (Part II) |                 |
+-----------------+-----------------+------------------+-----------------+
