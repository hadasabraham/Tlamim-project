// component
import SvgColor from '../../../components/svg-color';

// ----------------------------------------------------------------------

const icon = (name) => <SvgColor src={`/assets/icons/navbar/${name}.svg`} sx={{ width: 1, height: 1 }} />;

const navConfig = [
  {
    title: 'מועמדים',
    path: '/candidates',
    icon: icon('ic_user'),
  },
  {
    title: 'עריכת שלבים',
    path: '/stages',
    icon: icon('ic_stages'),
  },
];

export default navConfig;
