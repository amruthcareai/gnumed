/*
 * DemographicDataAccessSQLPlugin.java
 *
 * Created on June 21, 2004, 9:54 AM
 */

package org.gnumed.testweb1.adapters;

import java.util.Map;
import java.util.ResourceBundle;

import javax.naming.Context;
import javax.naming.InitialContext;
import javax.sql.DataSource;

import org.apache.commons.logging.Log;
import org.apache.commons.logging.LogFactory;
import org.apache.struts.action.PlugIn;
import org.apache.struts.config.PlugInConfig;
import org.gnumed.testweb1.data.DataObjectFactory;
import org.gnumed.testweb1.global.Constants;
import org.gnumed.testweb1.global.Util;
import org.gnumed.testweb1.persist.DataObjectFactoryUsing;
import org.gnumed.testweb1.persist.DemographicDataAccess;
import org.gnumed.testweb1.persist.HealthRecordAccess01;
import org.gnumed.testweb1.persist.ResourceBundleUsing;
import org.gnumed.testweb1.persist.scripted.ClinicalSQL;
import org.gnumed.testweb1.persist.scripted.DemographicDetailSQL;
import org.gnumed.testweb1.persist.scripted.ScriptedSQLClinicalAccess;
import org.gnumed.testweb1.persist.scripted.ScriptedSQLDemographicDataAccess;
import org.gnumed.testweb1.persist.scripted.gnumed1.DrugRefAccess;
/**
 *
 * @author  sjtan
 */
public class DataAccessSQLPlugIn extends BasicPlugin implements PlugIn {
    public final static String IMPL="impl";
    /** Creates a new instance of DemographicDataAccessSQLPlugin */
    public DataAccessSQLPlugIn() {
    }
    
    Log log = LogFactory.getLog(this.getClass());
    
    public void destroy() {
    }
    
    private void setDataObjectFactory( DataObjectFactoryUsing factoryUsing, DataObjectFactory factory) {
        factoryUsing.setDataObjectFactory(factory);
    }
    
    private void setResourceBundleUsing( ResourceBundleUsing user, ResourceBundle bundle) {
        user.setResourceBundle(bundle);
    }
    
    
    public void init(org.apache.struts.action.ActionServlet actionServlet, org.apache.struts.config.ModuleConfig moduleConfig) throws javax.servlet.ServletException {
        try {
            
            Context ctx = new InitialContext();
            Context ctx2 = (Context) ctx.lookup(Constants.JNDI_ROOT);
            
            DataSource dataSource = (DataSource) ctx2.lookup(Constants.JNDI_REF_POOLED_GNUMED_CONNECTIONS);
            log.info( this + " got " + dataSource);
            
            PlugInConfig dataFactoryPluginConfig = Util.findPluginConfig(moduleConfig, DataObjectFactoryPlugIn.class);
            PlugInConfig pluginConfig = Util.findPluginConfig(moduleConfig, this.getClass());
              
            DataObjectFactory factory = null;
            try {
                String dataObjectFactoryClassName = 
                    (String)dataFactoryPluginConfig.getProperties().get(Constants.Servlet.OBJECT_FACTORY);
                
                factory = (DataObjectFactory) Class.forName(dataObjectFactoryClassName).newInstance();
                
                log.info(this + " found the data object implementation " + dataObjectFactoryClassName);
                
            } catch (Exception e) {
                log.error(e);
            }
            
            ResourceBundle bundle = getResourceBundle(moduleConfig);
            
            try {
            		initializeDemographicAccess(actionServlet, dataSource, pluginConfig  , factory, bundle);
                
             } catch (Exception e) {
                log.error( "UNABLE TO SET '" +
                DemographicDataAccess.DEMOGRAPHIC_ACCESS  +
                "' of servlet context", e);
            }
             
             ScriptedSQLClinicalAccess scriptedClinicalAccess = null;
            try {
                  scriptedClinicalAccess = initializeClinicalAccess(actionServlet, dataSource, pluginConfig , factory, bundle);
                
            } catch (Exception e) {
                log.error(e);
            }
            
            try {
            		initializeHealthRecordAccess(actionServlet, dataSource, pluginConfig  , factory, scriptedClinicalAccess);
           
            } catch (Exception e) {
                log.error( "UNABLE TO SET '" + "HealthRecordAccess"
                   +
                "' of servlet context", e);
            }
             
        } catch(Exception e) {
            throw new javax.servlet.ServletException("Unable to set servlet attribute for pooled datasource", e);
        }
    }

	/**
	 * @param actionServlet
	 * @param dataSource
	 * @param map
	 * @param factory
	 * @param bundle
	 * @throws InstantiationException
	 * @throws IllegalAccessException
	 * @throws ClassNotFoundException
	 */
	private void initializeDemographicAccess(org.apache.struts.action.ActionServlet actionServlet, DataSource dataSource, 
			PlugInConfig dataAccessPluginConfig, DataObjectFactory factory, ResourceBundle bundle) throws InstantiationException, IllegalAccessException, ClassNotFoundException {
		String demoImplClassName =
		(String) dataAccessPluginConfig.getProperties().get(Constants.Plugin.DEMOGRAPHIC_SQL_PROVIDER);
		
		DemographicDetailSQL sqlScriptImpl =
			(DemographicDetailSQL) Class.forName(demoImplClassName).newInstance();
	
		((ResourceBundleUsing)sqlScriptImpl).setResourceBundle(bundle);
		
		 ((DataObjectFactoryUsing)sqlScriptImpl).setDataObjectFactory( factory);
		
		ScriptedSQLDemographicDataAccess dbAccess = new ScriptedSQLDemographicDataAccess();
		
		dbAccess.setDataSource(dataSource);

		dbAccess.setDemographicDetailSQL((DemographicDetailSQL) sqlScriptImpl);
		      
		actionServlet.getServletContext().setAttribute(Constants.Servlet.DEMOGRAPHIC_ACCESS , dbAccess );
	}

	/**
	 * @param actionServlet
	 * @param dataSource
	 * @param map
	 * @param factory
	 * @param bundle
	 * @return
	 * @throws InstantiationException
	 * @throws IllegalAccessException
	 * @throws ClassNotFoundException
	 */
	private ScriptedSQLClinicalAccess initializeClinicalAccess(org.apache.struts.action.ActionServlet actionServlet, 
				DataSource dataSource, PlugInConfig dataAccessPluginConfig, DataObjectFactory factory, ResourceBundle bundle) throws InstantiationException, IllegalAccessException, ClassNotFoundException {
		ScriptedSQLClinicalAccess scriptedClinicalAccess;
		String clinImplClassName=
		    
		        (String) dataAccessPluginConfig.getProperties().get(Constants.Plugin.CLINICAL_SQL_PROVIDER);
		
		
		ClinicalSQL clinSqlScriptImpl =
		    
		        (ClinicalSQL) Class.forName(clinImplClassName).newInstance();
            
		 ((ResourceBundleUsing) clinSqlScriptImpl).setResourceBundle( bundle);
		
		 ((DataObjectFactoryUsing) clinSqlScriptImpl).setDataObjectFactory(factory);
         
         
		scriptedClinicalAccess = new ScriptedSQLClinicalAccess();
		scriptedClinicalAccess.setDataSource(dataSource);
            scriptedClinicalAccess.setClinicalSQL(clinSqlScriptImpl);
            actionServlet.getServletContext().
            setAttribute(Constants.Servlet.CLINICAL_ACCESS , scriptedClinicalAccess);
		return scriptedClinicalAccess;
	}

	/**
	 * @param actionServlet
	 * @param dataSource
	 * @param map
	 * @param factory
	 * @param scriptedClinicalAccess
	 * @throws InstantiationException
	 * @throws IllegalAccessException
	 * @throws ClassNotFoundException
	 */
	private void initializeHealthRecordAccess(org.apache.struts.action.ActionServlet actionServlet, 
			DataSource dataSource, PlugInConfig dataAccessPluginConfig,
			DataObjectFactory factory, ScriptedSQLClinicalAccess scriptedClinicalAccess) 
						throws InstantiationException, IllegalAccessException, ClassNotFoundException {
		
		String implClassName =
		(String) dataAccessPluginConfig.getProperties().get(Constants.Plugin.HEALTH_RECORD_ACCESS_PROVIDER);
		
		
		HealthRecordAccess01 healthRecordAccess = 
		(HealthRecordAccess01) Class.forName(implClassName).newInstance();
		log.info("implClassName for health record access" + implClassName);
		 
		healthRecordAccess.setDataSource(dataSource);
		healthRecordAccess.setDataObjectFactory(factory);
		healthRecordAccess.setClinicalDataAccess(scriptedClinicalAccess);
		
		actionServlet.getServletContext().setAttribute(Constants.Servlet.HEALTH_RECORD_ACCESS , healthRecordAccess);
	}

	 private void initializeDrugRefAccess(org.apache.struts.action.ActionServlet actionServlet, 
			DataSource dataSource, PlugInConfig dataAccessPluginConfig,
			DataObjectFactory factory, DrugRefAccess drugRefAccess) 
						throws InstantiationException, IllegalAccessException, ClassNotFoundException {
		
		String implClassName =
		(String) dataAccessPluginConfig.getProperties().get(Constants.Plugin.DRUG_REF_ACCESS_PROVIDER);
		
		
		DrugRefAccess access = 
		(DrugRefAccess) Class.forName(implClassName).newInstance();
		log.info("implClassName for health record access" + implClassName);
		 
		access.setDataSource(dataSource);
		access.setDataObjectFactory(factory);
		 
		actionServlet.getServletContext().setAttribute(Constants.Servlet.DRUGREF_ACCESS , access);
	}

    
}
