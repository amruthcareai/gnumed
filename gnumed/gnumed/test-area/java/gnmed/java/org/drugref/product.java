/** Java class "product.java" generated from Poseidon for UML.
 *  Poseidon for UML is developed by <A HREF="http://www.gentleware.com">Gentleware</A>.
 *  Generated with <A HREF="http://jakarta.apache.org/velocity/">velocity</A> template engine.
 */
package org.drugref;

import java.util.*;
import org.gnumed.gmClinical.script_drug;

/**
 * <p>
 * 
 * </p>
 */
public class product {

  ///////////////////////////////////////
  // attributes


/**
 * <p>
 * Represents ...
 * </p>
 */
    private Double amount; 

/**
 * <p>
 * Represents ...
 * </p>
 */
    private String comment; 

/**
 * <p>
 * Represents ...
 * </p>
 */
    private Integer id; 

   ///////////////////////////////////////
   // associations

/**
 * <p>
 * 
 * </p>
 */
    public drug_element drug_element; 
/**
 * <p>
 * 
 * </p>
 */
    public drug_formulations drug_formulations; 
/**
 * <p>
 * 
 * </p>
 */
    public drug_units drug_units; 
/**
 * <p>
 * 
 * </p>
 */
    public drug_routes drug_routes; 
/**
 * <p>
 * 
 * </p>
 */
    public Collection package_size = new java.util.HashSet(); // of type package_size
/**
 * <p>
 * 
 * </p>
 */
    public link_product_component link_product_component; 
/**
 * <p>
 * 
 * </p>
 */
    public Collection drug_flags = new java.util.HashSet(); // of type drug_flags
/**
 * <p>
 * 
 * </p>
 */
    public Collection available = new java.util.HashSet(); // of type available
/**
 * <p>
 * 
 * </p>
 */
    public Collection subsidized_products = new java.util.HashSet(); // of type subsidized_products
/**
 * <p>
 * 
 * </p>
 */
    public script_drug script_drug; 


   ///////////////////////////////////////
   // access methods for associations

    public drug_element getDrug_element() {
        return drug_element;
    }
    public void setDrug_element(drug_element _drug_element) {
        if (this.drug_element != _drug_element) {
            if (this.drug_element != null) this.drug_element.removeProduct(this);
            this.drug_element = _drug_element;
            if (_drug_element != null) _drug_element.addProduct(this);
        }
    }
    public drug_formulations getDrug_formulations() {
        return drug_formulations;
    }
    public void setDrug_formulations(drug_formulations _drug_formulations) {
        if (this.drug_formulations != _drug_formulations) {
            if (this.drug_formulations != null) this.drug_formulations.removeProduct(this);
            this.drug_formulations = _drug_formulations;
            if (_drug_formulations != null) _drug_formulations.addProduct(this);
        }
    }
    public drug_units getDrug_units() {
        return drug_units;
    }
    public void setDrug_units(drug_units _drug_units) {
        this.drug_units = _drug_units;
    }
    public drug_routes getDrug_routes() {
        return drug_routes;
    }
    public void setDrug_routes(drug_routes _drug_routes) {
        this.drug_routes = _drug_routes;
    }
    public Collection getPackage_sizes() {
        return package_size;
    }
    public void addPackage_size(package_size _package_size) {
        if (! this.package_size.contains(_package_size)) {
            this.package_size.add(_package_size);
            _package_size.setProduct(this);
        }
    }
    public void removePackage_size(package_size _package_size) {
        boolean removed = this.package_size.remove(_package_size);
        if (removed) _package_size.setProduct((product)null);
    }
    public link_product_component getLink_product_component() {
        return link_product_component;
    }
    public void setLink_product_component(link_product_component _link_product_component) {
        if (this.link_product_component != _link_product_component) {
            if (this.link_product_component != null) this.link_product_component.removeProduct(this);
            this.link_product_component = _link_product_component;
            if (_link_product_component != null) _link_product_component.addProduct(this);
        }
    }
    public Collection getDrug_flagss() {
        return drug_flags;
    }
    public void addDrug_flags(drug_flags _drug_flags) {
        if (! this.drug_flags.contains(_drug_flags)) {
            this.drug_flags.add(_drug_flags);
            _drug_flags.addProduct(this);
        }
    }
    public void removeDrug_flags(drug_flags _drug_flags) {
        boolean removed = this.drug_flags.remove(_drug_flags);
        if (removed) _drug_flags.removeProduct(this);
    }
    public Collection getAvailables() {
        return available;
    }
    public void addAvailable(available _available) {
        if (! this.available.contains(_available)) {
            this.available.add(_available);
            _available.setProduct(this);
        }
    }
    public void removeAvailable(available _available) {
        boolean removed = this.available.remove(_available);
        if (removed) _available.setProduct((product)null);
    }
    public Collection getSubsidized_productss() {
        return subsidized_products;
    }
    public void addSubsidized_products(subsidized_products _subsidized_products) {
        if (! this.subsidized_products.contains(_subsidized_products)) {
            this.subsidized_products.add(_subsidized_products);
            _subsidized_products.setProduct(this);
        }
    }
    public void removeSubsidized_products(subsidized_products _subsidized_products) {
        boolean removed = this.subsidized_products.remove(_subsidized_products);
        if (removed) _subsidized_products.setProduct((product)null);
    }
    public script_drug getScript_drug() {
        return script_drug;
    }
    public void setScript_drug(script_drug _script_drug) {
        if (this.script_drug != _script_drug) {
            this.script_drug = _script_drug;
            if (_script_drug != null) _script_drug.setProduct(this);
        }
    }


  ///////////////////////////////////////
  // operations


/**
 * <p>
 * Represents ...
 * </p>
 */
    public Double getAmount() {        
        return amount;
    } // end getAmount        

/**
 * <p>
 * Represents ...
 * </p>
 */
    public void setAmount(Double _amount) {        
        amount = _amount;
    } // end setAmount        

/**
 * <p>
 * Represents ...
 * </p>
 */
    public String getComment() {        
        return comment;
    } // end getComment        

/**
 * <p>
 * Represents ...
 * </p>
 */
    public void setComment(String _comment) {        
        comment = _comment;
    } // end setComment        

/**
 * <p>
 * Represents ...
 * </p>
 */
    public Integer getId() {        
        return id;
    } // end getId        

/**
 * <p>
 * Represents ...
 * </p>
 */
    public void setId(Integer _id) {        
        id = _id;
    } // end setId        

} // end product





