from diffcalc.hkl.you.calculation import YouHklCalculator, I, _calc_angle_between_naz_and_qaz
from diffcalc.tools import  assert_matrix_almost_equal
from diffcalc.utils import Position, DiffcalcException
from math import pi, sin, cos
from nose.plugins.skip import SkipTest
from nose.tools import assert_almost_equal, raises #@UnresolvedImport
from tests.diffcalc.hkl.test_calcvlieg import createMockDiffractometerGeometry, createMockHardwareMonitor, createMockUbcalc
import math
from diffcalc.hkl.you.constraints import ConstraintManager

try:
    from Jama import Matrix
except ImportError:
    from diffcalc.npadaptor import Matrix

def isnan(n):
    # math.isnan was introduced only in python 2.6 and is not in Jython (2.5.2)
    try:
        return math.isnan(n)
    except AttributeError:
        return n != n # for Jython


TORAD=pi/180
TODEG=180/pi

x = Matrix([[1], [0], [0]])   
y = Matrix([[0], [1], [0]])   
z = Matrix([[0], [0], [1]])


class Test_anglesToVirtualAngles():
    
    def setup(self):
        self.calc = YouHklCalculator(createMockUbcalc(None), createMockDiffractometerGeometry(), createMockHardwareMonitor(), None)
        
    
    def check_angle(self, name, expected, mu=-99, delta=99, nu=99,
                     eta=99, chi=99, phi=99):
        """All in degrees"""
        pos = Position(mu, delta, nu, eta, chi, phi)
        pos.changeToRadians()
        assert_almost_equal(self.calc._anglesToVirtualAngles(pos, None)[name]*TODEG, expected)
        
    # theta     
    def test_theta0(self):
        self.check_angle('theta', 0, delta=0, nu=0)
        
    def test_theta1(self):
        self.check_angle('theta', 1, delta=2, nu=0)
        
    def test_theta2(self):
        self.check_angle('theta', 1, delta=0, nu=2)
        
    def test_theta3(self):
        self.check_angle('theta', 1, delta=-2, nu=0)
        
    def test_theta4(self):
        self.check_angle('theta', 1, delta=0, nu=-2)
        
    # qaz
    def test_qaz0_degenerate_case(self):
        self.check_angle('qaz', 0, delta=0, nu=0)

    def test_qaz1(self):
        self.check_angle('qaz', 90, delta=2, nu=0)

    def test_qaz2(self):
        self.check_angle('qaz', 90, delta=90, nu=0)

    def test_qaz3(self):
        self.check_angle('qaz', 0, delta=0, nu=1, )

    # Can't see one by eye        
    # def test_qaz4(self):
    #    pos = Position(delta=20*TORAD, nu=20*TORAD)#.inRadians()
    #    assert_almost_equal(self.calc._anglesToVirtualAngles(pos, None)['qaz']*TODEG, 45)

    #alpha
    def test_defaultReferenceValue(self):
        # The following tests depemd on this
        assert_matrix_almost_equal(self.calc.n_phi, Matrix([[0],[0],[1]]))

    def test_alpha0(self):
        self.check_angle('alpha', 0, mu=0, eta=0, chi=0, phi=0)

    def test_alpha1(self):
        self.check_angle('alpha', 0, mu=0, eta=0, chi=0, phi=10)

    def test_alpha2(self):
        self.check_angle('alpha', 0, mu=0, eta=0, chi=0, phi=-10)

    def test_alpha3(self):
        self.check_angle('alpha', 2, mu=2, eta=0, chi=0, phi=0)

    def test_alpha4(self):
        self.check_angle('alpha', -2, mu=-2, eta=0, chi=0, phi=0)

    def test_alpha5(self):
        self.check_angle('alpha', 2, mu=0, eta=90, chi=2, phi=0)
    
    #beta
    
    def test_beta0(self):
        self.check_angle('beta', 0, delta=0, nu=0, mu=0, eta=0, chi=0, phi=0)
    
    def test_beta1(self):
        self.check_angle('beta', 0, delta=10, nu=0, mu=0, eta=6, chi=0, phi=5)
    
    def test_beta2(self):
        self.check_angle('beta', 10, delta=0, nu=10, mu=0, eta=0, chi=0, phi=0)
    
    def test_beta3(self):
        self.check_angle('beta', -10, delta=0, nu=-10, mu=0, eta=0, chi=0, phi=0)
    
    def test_beta4(self):
        self.check_angle('beta', 5, delta=0, nu=10, mu=5, eta=0, chi=0, phi=0)
    
    # azimuth
    def test_naz0(self):
        self.check_angle('naz', 0, mu=0, eta=0, chi=0, phi=0)
        
    def test_naz1(self):
        self.check_angle('naz', 0, mu=0, eta=0, chi=0, phi=10)

    def test_naz3(self):
        self.check_angle('naz', 0, mu=10, eta=0, chi=0, phi=10)

    def test_naz4(self):
        self.check_angle('naz', 2, mu=0, eta=0, chi=2, phi=0)
          
    def test_naz5(self):
        self.check_angle('naz', -2, mu=0, eta=0, chi=-2, phi=0)
        
    #tau
    def test_tau0(self):
        self.check_angle('tau', 0, mu=0, delta=0, nu=0, eta=0, chi=0, phi=0)
        #self.check_angle('tau_from_dot_product', 90, mu=0, delta=0, nu=0, eta=0, chi=0, phi=0)

        
    def test_tau1(self):
        self.check_angle('tau', 90, mu=0, delta=20, nu=0, eta=10, chi=0, phi=0)
        #self.check_angle('tau_from_dot_product', 90, mu=0, delta=20, nu=0, eta=10, chi=0, phi=0)

        
    def test_tau2(self):
        self.check_angle('tau', 90, mu=0, delta=20, nu=0, eta=10, chi=0, phi=3)
        #self.check_angle('tau_from_dot_product', 90, mu=0, delta=20, nu=0, eta=10, chi=0, phi=3)     

    def test_tau3(self):
        self.check_angle('tau', 88, mu=0, delta=20, nu=0, eta=10, chi=2, phi=0)
        #self.check_angle('tau_from_dot_product', 88, mu=0, delta=20, nu=0, eta=10, chi=2, phi=0)
  
    def test_tau4(self):
        self.check_angle('tau', 92, mu=0, delta=20, nu=0, eta=10, chi=-2, phi=0)
        #self.check_angle('tau_from_dot_product', 92, mu=0, delta=20, nu=0, eta=10, chi=-2, phi=0)       
         
    def test_tau5(self):
        self.check_angle('tau', 10, mu=0, delta=0, nu=20, eta=0, chi=0, phi=0)
        #self.check_angle('tau_from_dot_product', 10, mu=0, delta=0, nu=20, eta=0, chi=0, phi=0)

    #psi
    def test_psi0(self):
        pos = Position(0,0,0,0,0,0)
        assert isnan(self.calc._anglesToVirtualAngles(pos, None)['psi'])
        
    def test_psi1(self):
        self.check_angle('psi', 90, mu=0, delta=11, nu=0, eta=0, chi=0, phi=0)

    def test_psi2(self):
        self.check_angle('psi', 100, mu=10, delta=.00000001, nu=0, eta=0, chi=0, phi=0)
    
    def test_psi3(self):
        self.check_angle('psi', 80, mu=-10, delta=.00000001, nu=0, eta=0, chi=0, phi=0)
        
    def test_psi4(self):
        self.check_angle('psi', 90, mu=0, delta=11, nu=0, eta=0, chi=0, phi=12.3)
        
    def test_psi5(self):
        #self.check_angle('psi', 0, mu=10, delta=.00000001, nu=0, eta=0, chi=90, phi=0)     
        pos = Position(0,.00000001,0,0,90,0)
        pos.changeToRadians()
        assert isnan(self.calc._anglesToVirtualAngles(pos, None)['psi'])
        
    def test_psi6(self):
        self.check_angle('psi', 90, mu=0, delta=0.00000001, nu=0, eta=90, chi=0, phi=0)
  
    def test_psi7(self):
        self.check_angle('psi', 92, mu=0, delta=0.00000001, nu=0, eta=90, chi=2, phi=0)
  
    def test_psi8(self):
        self.check_angle('psi', 88, mu=0, delta=0.00000001, nu=0, eta=90, chi=-2, phi=0)
  

class Test_calc_theta():
    
    def setup(self):
        self.calc = YouHklCalculator(createMockUbcalc(I.times(2*pi)),
                                     createMockDiffractometerGeometry(),
                                     createMockHardwareMonitor(),
                                     None)
        self.e = 12.398420 # 1 Angstrom
    
    def test_100(self):
        h_phi = Matrix([[1],[0],[0]])
        assert_almost_equal(self.calc._calc_theta(h_phi.times(2*pi), 1)*TODEG, 30)
    
    @raises(DiffcalcException)
    def test_too_short(self):
        h_phi = Matrix([[1],[0],[0]])
        self.calc._calc_theta(h_phi.times(0), 1)
        
    @raises(DiffcalcException)
    def test_too_long(self):
        h_phi = Matrix([[1],[0],[0]])
        self.calc._calc_theta(h_phi.times(2*pi), 10)
     
        

class Test_calc_remaining_reference_angles_given_one():
    
    # TODO: These are very incomplete due to either totally failing inutuition
    #       or code!
    def setup(self):
        self.calc = YouHklCalculator(createMockUbcalc(None),
                                     createMockDiffractometerGeometry(),
                                     createMockHardwareMonitor(),
                                     None)
    
    def check(self, name, value, theta, tau, psi_e, alpha_e, beta_e):
        # all in deg
        psi, alpha, beta = self.calc._calc_remaining_reference_angles_given_one(
            name, value*TORAD, theta*TORAD, tau*TORAD)
        print 'psi', psi*TODEG, ' alpha:', alpha*TODEG, ' beta:', beta*TODEG
        if psi_e is not None:
            assert_almost_equal(psi*TODEG, psi_e)
        if alpha_e is not None:
            assert_almost_equal(alpha*TODEG, alpha_e)
        if beta_e is not None:
            assert_almost_equal(beta*TODEG, beta_e)

    def test_psi_given0(self):
        self.check('psi', 90, theta=10, tau=90, psi_e=90,
                    alpha_e=0, beta_e=0) 

    def test_psi_given1(self):
        self.check('psi', 92, theta=0, tau=90, psi_e=92,
                    alpha_e=2, beta_e=-2)

    def test_psi_given3(self):
        self.check('psi', 88, theta=0, tau=90, psi_e=88,
                    alpha_e=-2, beta_e=2)
         
    def test_psi_given4(self):
        self.check('psi', 0, theta=0, tau=90, psi_e=0,
                    alpha_e=-90, beta_e=90)
         
    def test_psi_given4a(self):
        self.check('psi', 180, theta=0, tau=90, psi_e=180,
                    alpha_e=90, beta_e=-90)
        
    def test_psi_given5(self):
        raise SkipTest
        # TODO: I don't understand why this one passes!
        self.check('psi', 180, theta=0, tau=80,
                   psi_e=180, alpha_e=80, beta_e=-80)
        self.check('psi', 180, theta=0, tau=80,
                   psi_e=180, alpha_e=90, beta_e=-90)
        
    def test_a_eq_b0(self):
        self.check('a_eq_b', 9999, theta=0, tau=90,
                   psi_e=90, alpha_e=0, beta_e=0)
        
    def test_alpha_given(self):
        self.check('alpha', 2, theta=0, tau=90,
                   psi_e=92, alpha_e=2, beta_e=-2)
        
    def test_beta_given(self):
        self.check('beta', 2, theta=0, tau=90,
                   psi_e=88, alpha_e=-2, beta_e=2)
#    def test_a_eq_b1(self):
#        self.check('a_eq_b', 9999, theta=20, tau=90,
#                   psi_e=90, alpha_e=10, beta_e=10)
        
#    def test_psi_given0(self):
#        self.check('psi', 90, theta=10, tau=45, psi_e=90,
#                    alpha_e=7.0530221302831952, beta_e=7.0530221302831952)

    
class Test_calc_detector_angles_given_one():
    
    def setup(self):
        self.calc = YouHklCalculator(createMockUbcalc(None),
                                     createMockDiffractometerGeometry(),
                                     createMockHardwareMonitor(),
                                     None)
    def check(self, name, value, theta, delta_e, nu_e, qaz_e):
        # all in deg
        delta, nu, qaz = self.calc._calc_remaining_detector_angles_given_one(
            name, value*TORAD, theta*TORAD)
        assert_almost_equal(delta*TODEG, delta_e)
        assert_almost_equal(nu*TODEG, nu_e)
        if qaz_e is not None:
            assert_almost_equal(qaz*TODEG, qaz_e)
    
    def test_nu_given0(self):
        self.check('nu', 0, theta=3, delta_e=6, nu_e=0, qaz_e=90)
                
    def test_nu_given1(self):
        self.check('nu', 10, theta=7.0530221302831952, delta_e=10, nu_e=10, qaz_e=None)
        
    def test_nu_given2(self):
        self.check('nu', 6, theta=3, delta_e=0, nu_e=6, qaz_e=0)
        
    def test_delta_given0(self):
        self.check('delta', 0, theta=3, delta_e=0, nu_e=6, qaz_e=0)
        
    def test_delta_given1(self):
        self.check('delta', 10, theta=7.0530221302831952, delta_e=10, nu_e=10, qaz_e=None)
        
    def test_delta_given2(self):
        self.check('delta', 6, theta=3, delta_e=6, nu_e=0, qaz_e=90)
        
    def test_qaz_given0(self):
        self.check('qaz', 90, theta=3, delta_e=6, nu_e=0, qaz_e=90)
                
    def test_qaz_given2(self):
        self.check('qaz', 0, theta=3, delta_e=0, nu_e=6, qaz_e=0)


class Test_calc_angle_between_naz_and_qaz():
    
    def test1(self):
        diff = _calc_angle_between_naz_and_qaz(theta=0, alpha=0, tau=90*TORAD)
        assert_almost_equal(diff*TODEG, 90)
    
    def test2(self):
        diff = _calc_angle_between_naz_and_qaz(theta=0*TORAD, alpha=0, tau=80*TORAD)
        assert_almost_equal(diff*TODEG, 80)

   
class Test_calc_remaining_sample_angles_given_one():
    #_calc_remaining_detector_angles_given_one
    def setup(self):
        self.calc = YouHklCalculator(createMockUbcalc(None),
                                     createMockDiffractometerGeometry(),
                                     createMockHardwareMonitor(),
                                     None)
    
    def check(self, name, value, Q_lab, n_lab, Q_phi,  n_phi,
              phi_e, chi_e, eta_e, mu_e):
        phi, chi, eta, mu = self.calc._calc_remaining_sample_angles_given_one(
                            name, value*TORAD, Q_lab, n_lab, Q_phi, n_phi)
        print 'phi', phi*TODEG, ' chi:', chi*TODEG, ' eta:', eta*TODEG, ' mu:', mu*TODEG
        if phi_e is not None:
            assert_almost_equal(phi*TODEG, phi_e)
        if chi_e is not None:
            assert_almost_equal(chi*TODEG, chi_e)
        if eta_e is not None:
            assert_almost_equal(eta*TODEG, eta_e)
        if mu_e is not None:
            assert_almost_equal(mu*TODEG, mu_e)
   
    @raises(ValueError)
    def test_constrain_xx_degenerate(self):
        self.check('mu', 0, Q_lab=x, n_lab=x, Q_phi=x, n_phi=x,
                    phi_e=0, chi_e=0, eta_e=0, mu_e=0)
        
    def test_constrain_mu_0(self):
        raise SkipTest()
        self.check('mu', 0, Q_lab=x, n_lab=z, Q_phi=x, n_phi=z,
                    phi_e=0, chi_e=0, eta_e=0, mu_e=0)


    def test_constrain_mu_10(self):
        raise SkipTest()
        self.check('mu', 10, Q_lab=x, n_lab=z, Q_phi=x, n_phi=z,
                    phi_e=-90, chi_e=10, eta_e=-90, mu_e=10)
        
    def test_constrain_mu_n10(self):
        raise SkipTest()
        self.check('mu', -10, Q_lab=x, n_lab=z, Q_phi=x, n_phi=z,
                    phi_e=90, chi_e=10, eta_e=90, mu_e=-10)
        
    def test_constrain_eta_10_wasfailing(self):
        # Required the choice of a different equation
        self.check('eta', 10, Q_lab=x, n_lab=z, Q_phi=x, n_phi=z,
                    phi_e=-10, chi_e=0, eta_e=10, mu_e=0)
        
    def test_constrain_eta_n10(self):
        self.check('eta', -10, Q_lab=x, n_lab=z, Q_phi=x, n_phi=z,
                    phi_e=10, chi_e=0, eta_e=-10, mu_e=0)

    def test_constrain_eta_20_with_theta_20(self):
        theta = 20*TORAD
        Q_lab = Matrix([[cos(theta)], [-sin(theta)],[0]])
        self.check('eta', 20, Q_lab=Q_lab, n_lab=z, Q_phi=x, n_phi=z,
                    phi_e=0, chi_e=0, eta_e=20, mu_e=0)
        
    @raises(ValueError)
    def test_constrain_chi_0_degenerate(self):
        self.check('chi', 0, Q_lab=x, n_lab=z, Q_phi=x, n_phi=z,
                    phi_e=0, chi_e=0, eta_e=0, mu_e=0)

    def test_constrain_chi_10(self):
        self.check('chi', 10, Q_lab=x, n_lab=z, Q_phi=x, n_phi=z,
                    phi_e=-90, chi_e=10, eta_e=90, mu_e=-10)

    def test_constrain_chi_90(self):
        self.check('chi', 90, Q_lab=z.times(-1), n_lab=x, Q_phi=x, n_phi=z,
                    phi_e=0, chi_e=90, eta_e=0, mu_e=0)
        
    def test_constrain_phi_0(self):
        self.check('phi', 0, Q_lab=x, n_lab=z, Q_phi=x, n_phi=z,
                    phi_e=0, chi_e=0, eta_e=0, mu_e=0)

    def test_constrain_phi_10(self):
        self.check('phi', 10, Q_lab=x, n_lab=z, Q_phi=x, n_phi=z,
                    phi_e=10, chi_e=0, eta_e=-10, mu_e=0)

    def test_constrain_phi_n10(self):
        self.check('phi', -10, Q_lab=x, n_lab=z, Q_phi=x, n_phi=z,
                    phi_e=-10, chi_e=0, eta_e=10, mu_e=0)
        
    def test_constrain_phi_20_with_theta_20(self):
        theta = 20*TORAD
        Q_lab = Matrix([[cos(theta)], [-sin(theta)],[0]])
        self.check('phi', 20, Q_lab=Q_lab, n_lab=z, Q_phi=x, n_phi=z,
                    phi_e=20, chi_e=0, eta_e=0, mu_e=0)
