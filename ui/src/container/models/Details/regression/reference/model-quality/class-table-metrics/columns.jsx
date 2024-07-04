import { CHART_COLOR } from '@Helpers/common-chart-options';
import { numberFormatter } from '@Src/constants';

export default [
  {
    title: '',
    key: 'className',
    dataIndex: 'className',
    render: (label) => <div className="font-[var(--coo-font-weight-bold)]">{label}</div>,
  },
  {
    title: 'Reference Precision',
    key: 'precision',
    dataIndex: 'precision',
    align: 'right',
    width: '10rem',
    onCell: () => ({ style: { background: CHART_COLOR.REFERENCE_LIGHT } }),
    render: (precision) => numberFormatter().format(precision),
  },
  {
    title: 'Reference Recall',
    key: 'recall',
    dataIndex: 'recall',
    align: 'right',
    width: '10rem',
    onCell: () => ({ style: { background: CHART_COLOR.REFERENCE_LIGHT } }),
    render: (recall) => numberFormatter().format(recall),
  },
  {
    title: 'Reference F1-Score',
    key: 'fMeasure',
    dataIndex: 'fMeasure',
    align: 'right',
    width: '10rem',
    onCell: () => ({ style: { background: CHART_COLOR.REFERENCE_LIGHT } }),
    render: (fMeasure) => numberFormatter().format(fMeasure),
  },
  {
    title: 'Reference True Positive Rate',
    key: 'truePositiveRate',
    dataIndex: 'truePositiveRate',
    align: 'right',
    width: '10rem',
    onCell: () => ({ style: { background: CHART_COLOR.REFERENCE_LIGHT } }),
    render: (truePositiveRate) => numberFormatter().format(truePositiveRate),
  },
  {
    title: 'Reference False Positive Rate',
    key: 'falsePositiveRate',
    dataIndex: 'falsePositiveRate',
    align: 'right',
    width: '10rem',
    onCell: () => ({ style: { background: CHART_COLOR.REFERENCE_LIGHT } }),
    render: (falsePositiveRate) => numberFormatter().format(falsePositiveRate),
  },
];
