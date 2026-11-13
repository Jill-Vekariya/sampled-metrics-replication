"""Compile the review manuscript directly from executed experiment artifacts.

ReportLab source is the executable manuscript source; article.md is also emitted.
The optional official ReScience LaTeX class is not needed for this build.
"""
from pathlib import Path
import csv
import json
import html
import re
from reportlab.pdfgen import canvas
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Table,
                               TableStyle, Image, PageBreak, KeepTogether)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

ROOT = Path(__file__).resolve().parent
TITLE = '[Re] Ranking reversals under sampled recommendation metrics'
SUBTITLE = 'A scoped replication of the IJCAI 2021 illustrative experiment'
AUTHOR = 'Jill Vekariya'
EMAIL = 'jillvekariya.10@gmail.com'
CODE_URL = 'https://github.com/Jill-Vekariya/sampled-metrics-replication'
# Reference: ReScience/template, commit 0978d0e, rescience.cls lines 42-46.
# Adapt the geometry, red journal tag, left-aligned title and hierarchy.
PAGE_LEFT, PAGE_RIGHT = 4.5 * cm, 3.0 * cm
PAGE_TOP, PAGE_BOTTOM = 3.0 * cm, 3.5 * cm
TEXT_WIDTH = A4[0] - PAGE_LEFT - PAGE_RIGHT
JOURNAL_RED = '#CF232B'


def main():
    result = ROOT/'results/windows-final'
    s = json.loads((result/'summary.json').read_text())
    primary = {(r['model'],r['metric']):r for r in s['primary']}
    with (result/'curves.csv').open() as f: curves = list(csv.DictReader(f))
    out = ROOT/'manuscript'
    out.mkdir(exist_ok=True)
    fontroot=ROOT/'manuscript/fonts'
    for name,file in [('Body','DejaVuSerif.ttf'),('BodyItalic','DejaVuSerif-Italic.ttf'),
                      ('BodyBold','DejaVuSerif-Bold.ttf'),('Sans','DejaVuSans.ttf'),
                      ('SansBold','DejaVuSans-Bold.ttf'),('Mono','DejaVuSansMono.ttf')]:
        pdfmetrics.registerFont(TTFont(name,str(fontroot/file)))
    pdfmetrics.registerFontFamily('Body',normal='Body',bold='BodyBold',italic='BodyItalic',boldItalic='BodyBold')
    pdfmetrics.registerFontFamily('Sans',normal='Sans',bold='SansBold',italic='Sans',boldItalic='SansBold')
    styles=getSampleStyleSheet()
    styles.add(ParagraphStyle('Text',fontName='Body',fontSize=9.9,leading=13.0,spaceAfter=5.8))
    styles.add(ParagraphStyle('Title2',fontName='SansBold',fontSize=18.5,leading=23,spaceAfter=10))
    styles.add(ParagraphStyle('Sub',fontName='Sans',fontSize=10.0,leading=14,textColor=colors.HexColor('#555555'),spaceAfter=8))
    styles.add(ParagraphStyle('Head',fontName='SansBold',fontSize=12.7,leading=16,spaceBefore=10,spaceAfter=6,keepWithNext=True))
    styles.add(ParagraphStyle('Small2',fontName='Sans',fontSize=8.0,leading=10.3,spaceAfter=5))
    styles.add(ParagraphStyle('Cell',fontName='Sans',fontSize=7.6,leading=10))
    styles.add(ParagraphStyle('Code2',fontName='Mono',fontSize=7.5,leading=11,spaceAfter=8))
    story=[]; md=[]

    def markdown_text(value):
        # Convert ReportLab paragraph markup to readable GitHub Markdown.
        value = re.sub(r'<link href="([^"]+)">([^<]+)</link>', r'[\2](\1)', value)
        value = value.replace('<b>', '**').replace('</b>', '**')
        value = value.replace('<i>', '*').replace('</i>', '*')
        value = value.replace('<super>', '<sup>').replace('</super>', '</sup>')
        value = value.replace('<br/>', '\n')
        return html.unescape(value)

    def text(value,style='Text'):
        story.append(Paragraph(value,styles[style]))
        formatted = markdown_text(value)
        if style == 'Title2':
            formatted = '# ' + formatted
        elif style == 'Sub' and value == SUBTITLE:
            formatted = '*' + formatted + '*'
        md.extend([formatted, ''])
    def head(value):
        match = re.match(r'^(\d+)\.\s+(.+)$', value)
        formatted = (f'<font color="#A0A0A0">{match.group(1)}</font> {match.group(2)}'
                     if match else value)
        story.append(Paragraph(formatted,styles['Head']))
        md.extend(['## '+value, ''])

    def page():
        # Natural page flow with keepWithNext headings is closer to the
        # official template than forcing a page at every manuscript section.
        return None
    def table(headers,rows,widths=None,caption=None):
        data=[[Paragraph(html.escape(str(v)),styles['Cell']) for v in row] for row in [headers]+rows]
        if widths:
            widths = [TEXT_WIDTH * float(w) / sum(widths) for w in widths]
        t=Table(data,colWidths=widths,repeatRows=1,hAlign='LEFT')
        t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),colors.HexColor('#e9eef2')),
                              ('LINEBELOW',(0,0),(-1,0),.7,colors.HexColor('#7f8d99')),
                              ('LINEBELOW',(0,-1),(-1,-1),.5,colors.HexColor('#a9b1b8')),
                              ('VALIGN',(0,0),(-1,-1),'TOP'),('TOPPADDING',(0,0),(-1,-1),5),
                              ('BOTTOMPADDING',(0,0),(-1,-1),6),('LEFTPADDING',(0,0),(-1,-1),6)]))
        if caption:
            # Keep the table and its caption together in the narrow ReScience layout.
            story.append(KeepTogether([t, Spacer(1,4),
                                       Paragraph(caption,styles['Small2'])]))
        else:
            story.extend([t, Spacer(1,9)])
        md.extend(['| '+' | '.join(map(str,headers))+' |','|'+'---|'*len(headers)])
        md.extend('| '+' | '.join(map(str,row))+' |' for row in rows);md.append('')
        if caption:
            md.extend([markdown_text(caption),''])
    def figure(name,caption,height):
        path=ROOT/'figures/final'/name
        iw, ih = ImageReader(str(path)).getSize()
        width = TEXT_WIDTH
        scaled_height = width * ih / iw
        if scaled_height > height:
            width *= height / scaled_height
            scaled_height = height
        pic=Image(str(path),width=width,height=scaled_height)
        # A figure and its caption must not be separated by a page break.
        story.append(KeepTogether([pic, Spacer(1, 5), Paragraph(caption, styles['Small2'])]))
        md.extend([caption,'',f'![{caption}](../figures/final/{name})',''])
    def lookup(model,name,mode='with_replacement',correction='False'):
        return float(next(x['mean'] for x in curves if x['model']==model and x['metric']==name and
                          x['m']=='99' and x['mode']==mode and x['correction']==correction))
    abstract = ("An independent Python implementation is used to revisit the fixed-rank counterexample in "
        "Krichene and Rendle's IJCAI 2021 article. Finite-distribution expectations, 1000-repeat Monte Carlo "
        "evaluations and separate 100000-repeat checks reproduce the central ranking reversal. Full-catalogue "
        "average precision favors C over A (0.101379 versus 0.010000), whereas evaluating with 99 uniformly "
        "sampled negatives favors A over C (expected values 0.636592 versus 0.326169). Expected AUC is invariant "
        "to sample size. All 12 printed exact-metric values agree at the source's three-decimal precision. "
        "Secondary calculations retain the reversal without replacement and show remaining bias after a simple "
        "rank correction. The evidence concerns a designed five-instance example, not trained models or real users.")
    text(TITLE,'Title2');text(SUBTITLE,'Sub')
    text('<b>'+AUTHOR+'</b>','Sub')
    text('Independent researcher | 12 November 2026 | ReScience C replication manuscript','Small2')
    text('Correspondence: <link href="mailto:'+EMAIL+'">'+EMAIL+'</link>','Small2')
    head('Abstract');text(abstract)
    text('<b>Keywords:</b> recommender evaluation; sampled metrics; partial replication; Python','Small2')
    head('1. Objective and scope')
    text("The replication target is the numerical example in Tables 1 and 2 and the expectation curves in "
         "Figures 2 and 3 of the published IJCAI 2021 extended abstract [1]. Its narrow question is whether "
         "sampling irrelevant candidates can reverse a comparison between fixed recommender rankings, even "
         "after averaging out sampling noise. The source is a self-contained published result related to the "
         "authors' longer KDD 2020 paper [2].")
    text("Zhao et al.'s broader evaluation study [3] also examines how sampled candidates and evaluation "
         "settings affect comparisons between recommendation algorithms. The present target is narrower: "
         "the published fixed-rank counterexample isolates the metric calculation from model training and "
         "data splitting. It tests a specific numerical claim, rather than measuring the prevalence of "
         "ranking reversals across learned models or real-world datasets.")
    text("The contribution here is an independently executable verification package: exact expectations and "
         "macro-evaluation variances, random simulation, finite-catalogue correctness oracles, two operating "
         "systems and transparent comparison at unrounded precision. The fixture and the inconsistency claim "
         "are credited to the original authors; the phenomenon is not presented as a new discovery.")
    head('Replication significance')
    text("The published example makes a falsifiable claim about evaluation rankings, "
         "not the training of a particular recommender. We independently implement "
         "the finite sampled-rank distribution, derive expectations and variances, simulate sampling "
         "with predeclared seeds, and check the resulting model-order reversals against the source. "
         "Agreement of these different computational routes verifies that specific numerical "
         "counterexample; it does not establish the frequency of the effect in real systems.")
    page()
    head('2. Frozen computational protocol')
    text("The catalogue contains n=10000 items and exactly one relevant item for each of five evaluation "
         "instances. A, B and C are the source's constructed rank lists, not learned model implementations. "
         "Rank 1 is best. These numerical inputs require no user records, dataset download or training.")
    table(['List','Full-catalogue ranks of the five relevant items'],
          [['A','100, 100, 100, 100, 100'],['B','40, 40, 8437, 9266, 4482'],
           ['C','212, 2, 743, 5342, 1548']],[82,389])
    text("For one relevant item, AP(r)=1/r, NDCG(r)=1/log<sub>2</sub>(r+1), Recall@10(r)=1[r≤10], "
         "and AUC(r)=(n-r)/(n-1). All reported scores are arithmetic means across the five instances. "
         "The untruncated AP and NDCG definitions follow the source.")
    text("The primary protocol samples m irrelevant items uniformly with replacement, excluding the relevant "
         "item. If K sampled entries outrank the relevant item, its sampled rank is 1+K. With p=(r-1)/(n-1), "
         "K follows Binomial(m,p). Repeated draws count as repeated entries under this protocol. A sampled "
         "AUC therefore uses a catalogue size of m+1 and a denominator of m, rather than n-1.")
    text("Expected metrics are obtained by summing M(1+k)Pr(K=k), for k=0,...,m. The variance of a single "
         "five-instance macro evaluation is the sum of the five instance variances divided by 25, with draws "
         "independent across instances. SD below denotes the square root of this variance. The Monte Carlo "
         "standard error of an average over R repeated evaluations is SD/√R; the two quantities are distinct.")
    text("The configuration was frozen before final metric evaluation (protocol v1.0). The primary sample "
         "size is 99 negatives. One thousand repetitions use NumPy seeds 20261112, 20261113 and 20261114 "
         "for A, B and C. Separate 100000-repeat checks use those seeds plus 10000. Twenty-three declared "
         "sample sizes from 1 to 9999 support the sensitivity curves; no outcome-dependent tuning is used.")
    head('3. Independent implementation and checks')
    text("The code was written from the published definitions. NumPy provides random draws and SciPy provides "
         "binomial and hypergeometric mass functions. Exhaustive enumeration of all small-catalogue sequences "
         "and subsets checks those distributions. Separate direct negative-item sampling checks metric means. "
         "Other tests cover rank boundaries, exclusion of the positive, repeated negative draws, complete "
         "sampling, aggregation, fixed seeds, invalid inputs and the closed-form binomial AP expectation.")
    text("For AP, the independent closed-form oracle is [1-(1-p)<super>m+1</super>]/[(m+1)p] for p&gt;0, "
         "with limiting value 1 at p=0. Expected AUC must equal full-catalogue AUC. When m=1, every metric "
         "has expectation (1-p)M(1)+pM(2); Recall@10 is then constant, rather than a useful AUC comparison.")
    page()
    head('4. Primary replicated results')
    text("Table 1 reports independent full-catalogue calculations. All entries round to the values printed "
         "in the original Table 1. In particular, C has higher AP and NDCG than A, whereas A has higher AUC.")
    table(['Model','AUC','AP','NDCG','Recall@10'],[[model]+[
        f"{primary[model,name]['exact']:.6f}" for name in ['AUC','AP','NDCG','Recall@10']]
        for model in ['A','B','C']],[50,105,105,105,106],
        caption='<b>Table 1.</b> Independently calculated deterministic full-catalogue metrics.')
    text("With 99 sampled negatives, expected AP ranks A above B above C. Expected NDCG ranks A above C "
         "above B. Sampling reverses the A-versus-C comparison for both metrics, without requiring any "
         "particular random realization. The 1000-repeat AP estimates are 0.634902, 0.343412 and 0.325680 "
         "for A, B and C; the corresponding analytic expectations are shown in Table 2.")
    text("Each entry in Table 2 is an analytical expectation ± single-evaluation SD. "
         "It covers all four metrics in source Table 2, including AUC. These are "
         "conditional moments for five independent instances, not standard errors of the expectation.",'Small2')
    table(['Metric','A','B','C'],[
        [name]+[f"{primary[model,name]['expected']:.6f} ± {primary[model,name]['analytic_sd']:.6f}"
                for model in ['A','B','C']]
        for name in ['AUC','AP','NDCG','Recall@10']],[65,103,103,103],
        caption=('<b>Table 2.</b> Analytic expectation ± single-evaluation SD '
                 '(m=99 negatives, with replacement). Source simulation estimates '
                 'are compared in Section 6.'))
    figure('rank_reversal.png','Figure 1. Full-catalogue metrics, sampled expectations and 1000-repeat Monte Carlo means for the published rank fixture.',168)
    text("Across the declared uncorrected sample sizes and both sampling schemes, the largest absolute AUC "
         "expectation error is 1.23×10<super>-15</super> or less. Every calibration mean falls within five "
         "analytic Monte Carlo standard errors of its target (largest absolute standardized error below 1.2).")
    page()
    head('5. Sample-size sensitivity and secondary analyses')
    figure('sample_size_sensitivity.png','Figure 2. Recomputed expectation curves on the frozen sample-size grid. Dotted lines show each full-catalogue metric; line segments interpolate the evaluated points.',330)
    text("For AP, the computed orders are A&gt;C&gt;B at m=20, A&gt;B&gt;C at m=200, and C&gt;A&gt;B at m=500. "
         "These reproduce the source's illustrated changes. At m=9999, the order is C&gt;B&gt;A; full-catalogue "
         "B AP is 0.010089912 and A AP is 0.010000000. Their equality in the printed table is a "
         "three-decimal rounding effect. With-replacement sampling at m=n-1 does not exhaust the catalogue.")
    text("The prespecified without-replacement extension uses K~Hypergeometric(n-1,r-1,m). At m=99, "
         "expected AP is 0.635805, 0.340548 and 0.325970 for A, B and C, preserving the reversal. "
         "At m=9999, all four metrics for all three recommenders equal their exact full-catalogue values, "
         "as they must when every irrelevant item is included once.")
    text("The secondary Eq.9 correction evaluates the metric at floor[1+(n-1)K/m]. At m=99 with replacement, "
         "corrected AP is 0.378158, 0.272897 and 0.223821. This reduces AP's absolute bias for each "
         "fixture recommender, but still ranks A above C. This limited result concerns the simple rank "
         "correction, not the source's bias-variance estimators or its trained-model study.")
    page()
    head('6. Agreement, uncertainty and discrepancies')
    text("All primary directional checks pass. The source's Table 2 contains simulation estimates rather "
         "than exact expectations; its random seed is not specified in the selected article. For example, "
         "the source reports A's sampled AP as 0.630±0.129, compared with the independently calculated "
         "expectation 0.636592 and SD 0.130393. A repeated-evaluation mean need not match to three decimals.")
    text("No published Table 2 mean triggers the frozen diagnostic threshold: a 0.0005 rounding allowance "
         "plus 3.29 combined standard errors, conditional on the source's stated 1000 independent "
         "repetitions. This is a descriptive compatibility check, not proof of identical experimental code. "
         "The exact SDs, the new simulated SDs, source SDs and every mean difference are retained in CSV. "
         "No population p-value or user-bootstrap interval is appropriate for these five designed instances.")
    head('Replication evidence against the original')
    text("The replication was assessed against observable targets defined by the original "
         "IJCAI example. Success means agreement with its quantitative values or directional "
         "behavior under the same sampling assumptions; it does not imply a trained-model "
         "replication or an estimate of how frequently the effect occurs in practice.")
    table(['Source target', 'Independent check', 'Observed agreement'], [
        ['Table 1', '12 deterministic values', '12/12 match at source precision'],
        ['Table 2', 'All four metrics, m=99', 'Analytic moments; source means compatible'],
        ['Figure 2', 'AP ordering vs. m', 'Reversals at m=20, 200, 500 reproduced'],
        ['Figure 3', 'Metric-shape curves', 'Recall@5, AP, NDCG, AUC verified'],
        ['Analytic invariant', 'Expected sampled AUC', 'Invariant across sample sizes']
    ], [87, 125, 170])
    text("The accompanying REVIEWER_START_HERE.md maps each published target to "
         "machine-readable evidence, including documented simulation discrepancies. "
         "Plots use declared grids and are not claimed to be pixel-identical.",'Small2')
    head('7. Execution and reproducibility')
    text("The primary implementation was executed through Desktop Commander on a Windows 11 laptop with "
         "16 GB RAM and 12 logical processors, using Python 3.13.3, NumPy 2.5.4 and SciPy 1.18.1. "
         "The archived primary evaluation passed 40 tests at that time. An earlier run stopped before metric evaluation "
         "because Windows path separators broke a provenance lookup. The path serialization was corrected, "
         "the failure log retained and the experiment rerun; the scientific protocol was unchanged.")
    text("Linux execution (Python 3.12.14, NumPy 2.3.5, SciPy 1.17.0) agreed to numerical precision. "
         "A fresh Windows virtual environment installed pinned dependencies, passed the original 40 tests and "
         "repeated the experiment. Every primary summary and saved Monte Carlo array matched the first "
         "Windows run exactly. The later maintained repository passed 142 tests on 14 November 2026. "
         "This expanded suite is a post-submission software validation, not part of the frozen initial run. "
         "Source and protocol hashes, Git commits, seeds, software versions, timings "
         "and the detailed reproduction report accompany the package.")
    text('python -m pip install -r requirements.txt<br/>'
         'python -m pip install -r requirements-manuscript.txt<br/>python -m pytest -q<br/>'
         'python run_experiments.py --output results/new-run<br/>'
         'python build_manuscript.py','Code2')
    text("Run from the project root, following REVIEWER_START_HERE.md. Use a new output directory "
         "to protect the archived evidence. The builder regenerates manuscript tables from "
         "the preserved Windows results; compare_results.py audits an independent rerun.")
    head('8. Limitations and conclusion')
    text("This is a partial replication of an intentionally designed counterexample. It provides no estimate "
         "of prevalence in deployed systems, no performance benchmark, no evidence about training quality, "
         "and no reproduction of corrected-metric success rates on real data. The five instances have "
         "independent candidate draws; shared candidate sets would require a different variance calculation. "
         "The literature and journal overlap searches are documented but do not prove novelty or editorial suitability.")
    text("The independent calculations support the published result: sampling can reverse a model "
         "comparison in expectation, and repeatedly evaluating a biased sampled metric does not "
         "recover the full-catalogue comparison. The code and numerical oracles make this testable.")
    page()
    head('Appendix. Metric-shape verification')
    figure('metric_shape.png','Figure 3. Independent reconstruction of source Figure 3: expected sampled metrics including Recall@5 (rather than Recall@10), shown through rank 1000 of n=10000.',285)
    text("The source Figure 3 uses Recall@5, while its Tables 1-2 and Figure 2 use Recall@10. "
         "Only the reconstructed Figure 3 panel uses Recall@5; all original primary calculations, "
         "sample sizes and simulation records remain unchanged.",'Small2')
    head('Availability and declarations')
    text("Code and data availability: the accompanying research package includes the independent "
         "implementation, the attributed numerical fixture, results, figures, tests and reproduction instructions. "
         "Repository: "+CODE_URL+". "
         "No third-party article PDF or real-user dataset is included "
         "in the release archive. The independent code is licensed under MIT and the manuscript under CC BY 4.0.",'Small2')
    text("The author declares no competing interests and no external research funding, "
         "no simultaneous journal submission, and no close collaboration with the original authors. "
         "The author reviewed and accepts responsibility for the computations, interpretations, "
         "source code and manuscript.",'Small2')
    text("Assistance disclosure: ChatGPT contributed to coding, computational checks and "
         "draft preparation; the author is responsible for all final claims. The numerical "
         "results and methods can be independently inspected and reproduced.",'Small2')
    head('References')
    refs=[
      '[1] W. Krichene and S. Rendle. On Sampled Metrics for Item Recommendation (Extended Abstract). Proceedings of IJCAI 2021, pp. 4784-4788. DOI: 10.24963/ijcai.2021/651. Primary replication target.',
      '[2] W. Krichene and S. Rendle. On Sampled Metrics for Item Recommendation. Proceedings of KDD 2020, pp. 1748-1757. DOI: 10.1145/3394486.3403226. Related full publication; its real-data experiment is outside scope.',
      '[3] W. X. Zhao, Z. Lin, Z. Feng, P. Wang and J.-R. Wen. A Revisiting Study of Appropriate Offline Evaluation for Top-N Recommendation Algorithms. ACM Transactions on Information Systems 41(2), article 32 (online 2022). DOI: 10.1145/3545796. Initial target assessed during feasibility selection.']
    for r in refs:text(r,'Small2')
    def decorate(c,doc):
        # Journal-branded margin tag adapted from official header.tex.
        c.setFillColor(colors.HexColor(JOURNAL_RED))
        c.rect(0, A4[1]-44*cm/10, 3.75*cm, 1.0*cm, fill=1, stroke=0)
        c.setFillColor(colors.white); c.setFont('SansBold',8.8)
        c.drawCentredString(1.875*cm, A4[1]-40.8*cm/10, 'RESCIENCE C')
        c.setFillColor(colors.HexColor('#555555')); c.setFont('Sans',8.0)
        c.drawRightString(A4[0]-PAGE_RIGHT, A4[1]-1.5*cm,
                          'Replication / machine learning')
        c.setStrokeColor(colors.HexColor('#cccccc'))
        c.line(PAGE_LEFT, 1.45*cm, A4[0]-PAGE_RIGHT, 1.45*cm)
        c.setFont('Sans',7.5)
        c.drawString(PAGE_LEFT, 1.0*cm, 'ReScience C — replication')
        c.drawRightString(A4[0]-PAGE_RIGHT, 1.0*cm, str(doc.page))
    doc=SimpleDocTemplate(str(out/'article.pdf'),pagesize=A4,
                          leftMargin=PAGE_LEFT,rightMargin=PAGE_RIGHT,
                          topMargin=PAGE_TOP,bottomMargin=PAGE_BOTTOM,
                          title=TITLE,author=AUTHOR)
    doc.build(story,onFirstPage=decorate,onLaterPages=decorate)
    (out/'article.md').write_bytes('\n'.join(md).encode('utf-8'))
    metadata={'title':TITLE,'authors':[{'name':AUTHOR,'orcid':'','email':EMAIL,'affiliations':'1,*'}],
      'affiliations':[{'code':1,'name':'Independent researcher','address':''}],
      'keywords':'recommender systems, sampled metrics, partial replication, Python',
      'code':[{'url':CODE_URL},{'doi':''},{'swh':'swh:1:snp:f8731f1851a899e32443bd1b093bfb896188d3e1'}],
      'data':[{'url':CODE_URL+'/tree/main/results/windows-final'},{'doi':''}],
      'replication':[{'cite':refs[0][4:]},{'bib':'krichene2021'},{'url':'https://www.ijcai.org/proceedings/2021/0651.pdf'},
                     {'doi':'10.24963/ijcai.2021/651'}],
      'abstract':abstract,'bibliography':'bibliography.bib','type':'Replication','domain':'Machine Learning',
      'language':'Python','review':[{'url':(json.loads((ROOT/'publication/submission_receipt.json').read_text()).get('issue_url','') if (ROOT/'publication/submission_receipt.json').exists() else '')}],
      'contributors':[{'name':'','orcid':'','role':x} for x in ['editor','reviewer','reviewer']],
      'dates':[{'received':''},{'accepted':''},{'published':''}],
      'article':[{'number':''},{'doi':''},{'url':''}],
      'journal':[{'name':'ReScience C'},{'issn':'2430-3658'},{'volume':''},{'issue':''}]}
    import yaml
    class QuotedAbstract(str):
        pass
    yaml.SafeDumper.add_representer(QuotedAbstract, lambda dumper,value:
        dumper.represent_scalar('tag:yaml.org,2002:str',value,style='"'))
    metadata['abstract'] = QuotedAbstract(abstract)
    (out/'metadata.yaml').write_bytes((
        '# Author-approved replication manuscript. Editorial fields await the journal.\n'
        + yaml.safe_dump(metadata,sort_keys=False,allow_unicode=True)
    ).replace('\r\n', '\n').encode('utf-8'))
    print('Compiled',out/'article.pdf')


if __name__=='__main__': main()
