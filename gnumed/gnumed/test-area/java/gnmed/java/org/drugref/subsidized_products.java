/** Java class "subsidized_products.java" generated from Poseidon for UML.
 *  Poseidon for UML is developed by <A HREF="http://www.gentleware.com">Gentleware</A>.
 *  Generated with <A HREF="http://jakarta.apache.org/velocity/">velocity</A> template engine.
 */
package org.drugref;

import java.util.*;

/**
 * <p>
 * 
 * </p>
 */
public class subsidized_products {

  ///////////////////////////////////////
  // attributes


/**
 * <p>
 * Represents ...
 * </p>
 */
    private Integer quantity; 

/**
 * <p>
 * Represents ...
 * </p>
 */
    private Integer max_rpt; 

/**
 * <p>
 * Represents ...
 * </p>
 */
    private Double copayment; 

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
    private String restriction; 

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
    public product product; 
/**
 * <p>
 * 
 * </p>
 */
    public subsidies subsidies; 


   ///////////////////////////////////////
   // access methods for associations

    public product getProduct() {
        return product;
    }
    public void setProduct(product _product) {
        if (this.product != _product) {
            if (this.product != null) this.product.removeSubsidized_products(this);
            this.product = _product;
            if (_product != null) _product.addSubsidized_products(this);
        }
    }
    public subsidies getSubsidies() {
        return subsidies;
    }
    public void setSubsidies(subsidies _subsidies) {
        if (this.subsidies != _subsidies) {
            if (this.subsidies != null) this.subsidies.removeSubsidized_products(this);
            this.subsidies = _subsidies;
            if (_subsidies != null) _subsidies.addSubsidized_products(this);
        }
    }


  ///////////////////////////////////////
  // operations


/**
 * <p>
 * Represents ...
 * </p>
 */
    public Integer getQuantity() {        
        return quantity;
    } // end getQuantity        

/**
 * <p>
 * Represents ...
 * </p>
 */
    public void setQuantity(Integer _quantity) {        
        quantity = _quantity;
    } // end setQuantity        

/**
 * <p>
 * Represents ...
 * </p>
 */
    public Integer getMax_rpt() {        
        return max_rpt;
    } // end getMax_rpt        

/**
 * <p>
 * Represents ...
 * </p>
 */
    public void setMax_rpt(Integer _max_rpt) {        
        max_rpt = _max_rpt;
    } // end setMax_rpt        

/**
 * <p>
 * Represents ...
 * </p>
 */
    public Double getCopayment() {        
        return copayment;
    } // end getCopayment        

/**
 * <p>
 * Represents ...
 * </p>
 */
    public void setCopayment(Double _copayment) {        
        copayment = _copayment;
    } // end setCopayment        

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
    public String getRestriction() {        
        return restriction;
    } // end getRestriction        

/**
 * <p>
 * Represents ...
 * </p>
 */
    public void setRestriction(String _restriction) {        
        restriction = _restriction;
    } // end setRestriction        

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

} // end subsidized_products





